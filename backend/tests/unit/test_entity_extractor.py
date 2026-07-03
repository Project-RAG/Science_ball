import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock

from app.services.nlp.entity_extractor import EntityExtractor
from app.services.nlp.dictionaries import get_flattened_dictionary
from app.services.nlp.entity_extraction_service import EntityExtractionService
from app.repositories.entities import EntitiesRepository


def test_entity_extractor_basic():
    """Test basic dictionary extraction."""
    lookup = get_flattened_dictionary()
    extractor = EntityExtractor(lookup)

    text = "Nickel electrowinning is used in Canada."
    # Expected: nickel (Material), electrowinning (Process), canada (Location)
    spans = extractor.extract(text)

    span_texts = [s.text for s in spans]
    assert "Ni" in span_texts # 'Nickel' contains 'Ni' and the dict has 'Ni' as alias
    assert "electrowinning" in span_texts
    assert "Canada" in span_texts


def test_entity_extractor_aliases():
    """Test that aliases are correctly resolved to canonical names."""
    lookup = get_flattened_dictionary()
    extractor = EntityExtractor(lookup)

    text = "Никелевая руда и электролитическое извлечение."
    spans = extractor.extract(text)

    # 'никелевая руда' -> nickel, 'электролитическое извлечение' -> electrowinning
    assert any(s.canonical_name == "nickel" for s in spans)
    assert any(s.canonical_name == "electrowinning" for s in spans)


def test_entity_extractor_longest_match():
    """Test that the extractor prefers longer matches over shorter ones."""
    # Mock a dictionary where 'Nickel' and 'Nickel Ore' are both present
    lookup = {
        "nickel": {"canonical": "nickel", "type": "Material"},
        "nickel ore": {"canonical": "nickel_ore", "type": "Material"},
    }
    extractor = EntityExtractor(lookup)

    text = "This is nickel ore."
    spans = extractor.extract(text)

    # Should match 'nickel ore', not 'nickel'
    assert len(spans) == 1
    assert spans[0].text == "nickel ore"


@pytest.mark.asyncio
async def test_entity_extraction_service_integration():
    """Test the service orchestration with repository."""
    mock_repo = MagicMock(spec=EntitiesRepository)
    mock_repo.delete_by_document = AsyncMock()
    mock_repo.create_many = AsyncMock()

    service = EntityExtractionService(entities_repository=mock_repo)

    doc_id = uuid4()
    chunks = [
        {"id": uuid4(), "text": "Nickel electrowinning in Canada."},
        {"id": uuid4(), "text": "High temperature is required."}
    ]
    access_level = "internal"

    session = AsyncMock()
    await service.process_document_chunks(
        session=session,
        document_id=doc_id,
        chunks=chunks,
        access_level=access_level
    )

    # Check idempotency delete - use any mock for the session part
    args, _ = mock_repo.delete_by_document.call_args
    assert args[1] == doc_id

    # Check bulk creation
    mock_repo.create_many.assert_called_once()
    # In our service, create_many is called as: await self.entities_repository.create_many(session, all_entities_to_save)
    # So the first positional argument should be the session (AsyncMock), and the second should be the list.
    pos_args, _ = mock_repo.create_many.call_args
    entities_data = pos_args[1]

    assert isinstance(entities_data, list)
    assert len(entities_data) >= 3
    assert any(e["canonical_name"] == "nickel" for e in entities_data)
    assert any(e["canonical_name"] == "electrowinning" for e in entities_data)
    assert any(e["canonical_name"] == "canada" for e in entities_data)
    assert entities_data[0]["document_id"] == doc_id
    assert all(e["extraction_method"] == "dictionary" for e in entities_data)
