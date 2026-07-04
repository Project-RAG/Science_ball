from __future__ import annotations

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.schemas.search import EvidenceItem

class AnswerRequest(BaseModel):
    """Request for synthesized answer grounded in evidence."""
    query: str = Field(..., min_length=1, description="The natural language query")
    filters: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional filters to restrict search (e.g., year_from, practice_region)"
    )

class AnswerSummary(BaseModel):
    """Synthesized summary with a confidence score."""
    summary: str = Field(..., description="The synthesized answer text")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in the synthesis based on evidence quality")

class Citation(BaseModel):
    """Reference to a specific piece of evidence."""
    source_id: str = Field(..., description="The chunk_id of the source")
    document_title: str = Field(..., description="Title of the document containing the evidence")

class AnswerResponse(BaseModel):
    """Final response providing synthesized answer and traceability."""
    answer: AnswerSummary
    evidence: List[EvidenceItem] = Field(
        default_factory=list,
        description="The set of evidence items actually used to construct the answer"
    )
    contradictions: List[str] = Field(
        default_factory=list,
        description="List of identified contradictions between different sources"
    )
    knowledge_gaps: List[str] = Field(
        default_factory=list,
        description="Identified gaps where the evidence is insufficient to fully answer the query"
    )
    sources: List[Citation] = Field(
        default_factory=list,
        description="Simplified list of citations for the final response"
    )
