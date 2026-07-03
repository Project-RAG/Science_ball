import pytest
from unittest import mock
from backend.app.search.index_names import ESIndexNames
from backend.app.search.mappings import MAPPINGS
from backend.app.search.index_manager import ElasticsearchIndexManager

@pytest.mark.asyncio
async def test_mappings_structure():
    """Verify that all required indices have a mapping and include access_level."""
    required_indices = [
        ESIndexNames.DOCS,
        ESIndexNames.CHUNKS,
        ESIndexNames.FACTS,
        ESIndexNames.ENTITIES,
        ESIndexNames.EXPERIMENTS,
        ESIndexNames.EXPERTS
    ]

    for index in required_indices:
        assert index in MAPPINGS, f"Mapping missing for {index}"
        mapping = MAPPINGS[index]
        # mappings can be just the mapping dict or contain 'mappings' key
        props = mapping.get("mappings", {}).get("properties", mapping.get("properties", {}))
        assert "access_level" in props, f"access_level missing in mapping for {index}"
        assert props["access_level"]["type"] == "keyword", f"access_level must be keyword in {index}"

@pytest.mark.asyncio
async def test_chunks_mapping_special_fields():
    """Verify specific requirements for chunks index."""
    chunk_props = MAPPINGS[ESIndexNames.CHUNKS]["mappings"]["properties"]

    # Vector search
    assert "embedding" in chunk_props
    assert chunk_props["embedding"]["type"] == "dense_vector"

    # Nested numeric conditions
    assert "numeric_conditions" in chunk_props
    assert chunk_props["numeric_conditions"]["type"] == "nested"

@pytest.mark.asyncio
async def test_index_manager_create_if_not_exists():
    """Test the logic of creating an index only if it doesn't exist."""
    mock_es = mock.AsyncMock()
    manager = ElasticsearchIndexManager(mock_es)

    # Case 1: Index already exists
    mock_es.indices.exists.return_value = True
    result = await manager.create_index_if_not_exists("test_index", {})
    assert result is True
    mock_es.indices.create.assert_not_called()

    # Case 2: Index does not exist
    mock_es.indices.exists.return_value = False
    result = await manager.create_index_if_not_exists("test_index", {"settings": {}})
    assert result is True
    mock_es.indices.create.assert_called_once_with(
        index="test_index",
        body={"settings": {}}
    )

@pytest.mark.asyncio
async def test_setup_all_indices():
    """Test bulk setup of indices."""
    mock_es = mock.AsyncMock()
    manager = ElasticsearchIndexManager(mock_es)

    mock_es.indices.exists.return_value = False
    configs = {
        "index1": {"mappings": {}},
        "index2": {"mappings": {}}
    }

    results = await manager.setup_all_indices(configs)
    assert results == {"index1": True, "index2": True}
    assert mock_es.indices.create.call_count == 2
