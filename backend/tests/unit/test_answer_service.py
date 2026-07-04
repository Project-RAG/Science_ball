import pytest
from unittest.mock import MagicMock, AsyncMock
from app.services.answers.answer_service import AnswerService
from app.schemas.answers import AnswerRequest, AnswerResponse
from app.schemas.search import EvidenceItem, DocumentMetadata
from app.search.search_service import SearchService
from app.schemas.search import SearchResponse

@pytest.fixture
def mock_search_service():
    return AsyncMock(spec=SearchService)

@pytest.fixture
def answer_service(mock_search_service):
    return AnswerService(search_service=mock_search_service)

@pytest.fixture
def sample_evidence():
    return [
        EvidenceItem(
            chunk_id="chunk_1",
            document_id="doc_1",
            text="The optimal flow velocity for nickel electrowinning is 0.2 m/s.",
            confidence=0.9,
            metadata=DocumentMetadata(
                document_id="doc_1",
                title="Nickel Guide",
                source_type="publication"
            )
        ),
        EvidenceItem(
            chunk_id="chunk_2",
            document_id="doc_2",
            text="Some sources suggest 0.3 m/s is better for specific conditions.",
            confidence=0.7,
            metadata=DocumentMetadata(
                document_id="doc_2",
                title="Advanced Metallurgy",
                source_type="publication"
            )
        )
    ]

@pytest.mark.asyncio
async def test_synthesize_answer_success(answer_service, mock_search_service, sample_evidence):
    # Setup search service to return evidence
    mock_search_service.search.return_value = SearchResponse(
        query="What is the optimal flow velocity?",
        results=sample_evidence,
        total_hits=2,
        execution_time_ms=10.0
    )

    request = AnswerRequest(query="What is the optimal flow velocity?")
    response = await answer_service.synthesize_answer(request, ["public", "internal"])

    assert isinstance(response, AnswerResponse)
    assert response.answer.summary != ""
    # Since we are using the real llm_gateway which defaults to MockLLMProvider in dev/test,
    # it should return a mock answer that likely contains citations if our prompt is followed.
    # We check if at least one evidence item was tracked as used (if the mock LLM puts [chunk_x] in text).
    # Note: If MockLLMProvider just returns "Mock response", we might not have citations.
    # Let's check the actual result.

@pytest.mark.asyncio
async def test_synthesize_answer_no_evidence(answer_service, mock_search_service):
    # Setup search service to return no results
    mock_search_service.search.return_value = SearchResponse(
        query="Unknown topic",
        results=[],
        total_hits=0,
        execution_time_ms=5.0
    )

    request = AnswerRequest(query="What is the optimal flow velocity?")
    response = await answer_service.synthesize_answer(request, ["public", "internal"])

    assert "No relevant evidence" in response.answer.summary
    assert len(response.evidence) == 0
    assert len(response.sources) == 0

@pytest.mark.asyncio
async def test_synthesize_answer_error_handling(answer_service, mock_search_service):
    # Setup search service to raise exception
    mock_search_service.search.side_effect = Exception("Search failed")

    request = AnswerRequest(query="What is the optimal flow velocity?")

    # We expect the service to handle it or let it propagate depending on implementation
    # In our current AnswerService, search is called without a try-except around it directly
    # but synthesize_answer might be wrapped in route.
    # Let's check if we need a try-except in the service.
    with pytest.raises(Exception):
        await answer_service.synthesize_answer(request, ["public", "internal"])
