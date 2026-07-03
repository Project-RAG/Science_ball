from pydantic import BaseModel, Field
from typing import Optional, Dict

class ConfidenceBreakdown(BaseModel):
    """Detailed breakdown of how a confidence score was calculated."""
    extraction_score: float = Field(..., description="Score based on the extraction method used")
    source_reliability: float = Field(..., description="Score based on the reliability of the source document")
    supporting_sources_score: float = Field(0.0, description="Score based on corroboration from other sources")
    expert_verification_score: float = Field(0.0, description="Score based on human expert verification")
    llm_cap_applied: bool = Field(False, description="Whether the LLM confidence cap was applied to this score")

class ConfidenceResult(BaseModel):
    """The final calculated confidence result."""
    score: float = Field(..., ge=0.0, le=1.0, description="Final aggregated confidence score (0.0 to 1.0)")
    breakdown: ConfidenceBreakdown
    explanation: str = Field(..., description="Human-readable explanation of the score")
