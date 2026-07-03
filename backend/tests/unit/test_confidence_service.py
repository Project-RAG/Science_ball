import pytest
from app.services.nlp.confidence_service import ConfidenceService

@pytest.fixture
def service():
    return ConfidenceService()

def test_deterministic_high_confidence(service):
    # Manual extraction from publication, expert verified, multiple supporting sources
    result = service.calculate_fact_confidence(
        extraction_method="manual",
        source_type="publication",
        supporting_sources_count=3,
        is_expert_verified=True
    )
    # (0.35 * 1.0) + (0.25 * 0.9) + (0.20 * 1.0) + (0.20 * 1.0) = 0.35 + 0.225 + 0.2 + 0.2 = 0.975
    assert result.score == 0.975
    assert result.breakdown.llm_cap_applied is False

def test_weak_confidence(service):
    # LLM extraction from handbook, no supporting sources, not verified
    result = service.calculate_fact_confidence(
        extraction_method="llm",
        source_type="handbook",
        supporting_sources_count=0,
        is_expert_verified=False
    )
    # (0.35 * 0.7) + (0.25 * 0.6) + (0.20 * 0.0) + (0.20 * 0.0) = 0.245 + 0.15 = 0.395
    assert result.score == 0.395
    assert "Capped" not in result.explanation

def test_llm_cap_applied(service):
    # LLM extraction from publication, many supporting sources (should trigger cap)
    result = service.calculate_fact_confidence(
        extraction_method="llm",
        source_type="publication",
        supporting_sources_count=5,
        is_expert_verified=False
    )
    # Raw: (0.35 * 0.7) + (0.25 * 0.9) + (0.20 * 1.0) + (0.20 * 0.0) = 0.245 + 0.225 + 0.2 = 0.67
    # Should be capped to 0.65
    assert result.score == 0.65
    assert result.breakdown.llm_cap_applied is True
    assert "Capped due to LLM-only extraction" in result.explanation

def test_llm_no_cap_when_verified(service):
    # LLM extraction but expert verified -> cap should NOT apply
    result = service.calculate_fact_confidence(
        extraction_method="llm",
        source_type="publication",
        supporting_sources_count=5,
        is_expert_verified=True
    )
    # Raw: (0.35 * 0.7) + (0.25 * 0.9) + (0.20 * 1.0) + (0.20 * 1.0) = 0.245 + 0.225 + 0.2 + 0.2 = 0.87
    assert result.score == 0.87
    assert result.breakdown.llm_cap_applied is False

def test_unknown_source_and_method(service):
    # Test defaults for unknown inputs
    result = service.calculate_fact_confidence(
        extraction_method="mystery_tech",
        source_type="random_blog",
        supporting_sources_count=0,
        is_expert_verified=False
    )
    # ext: 0.5, src: 0.5, supp: 0.0, exp: 0.0
    # (0.35 * 0.5) + (0.25 * 0.5) = 0.175 + 0.125 = 0.3
    assert result.score == 0.3
