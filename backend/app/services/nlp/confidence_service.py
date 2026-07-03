from typing import Dict, Optional
import logging
from app.schemas.confidence import ConfidenceResult, ConfidenceBreakdown

logger = logging.getLogger(__name__)

class ConfidenceService:
    """
    Service for calculating confidence scores for extracted facts and entities.
    Implements the MVP formula defined in SDD section 10.
    """

    # Weights from SDD
    WEIGHT_EXTRACTION = 0.35
    WEIGHT_SOURCE = 0.25
    WEIGHT_SUPPORTING = 0.20
    WEIGHT_EXPERT = 0.20

    # LLM Cap: facts extracted only by LLM cannot exceed 0.65 without expert verification
    LLM_CONFIDENCE_CAP = 0.65

    # Base reliability scores for source types
    SOURCE_RELIABILITY = {
        "publication": 0.9,
        "patent": 0.8,
        "experiment": 0.8,
        "internal_report": 0.7,
        "handbook": 0.6,
    }

    # Base scores for extraction methods
    EXTRACTION_SCORES = {
        "manual": 1.0,
        "dictionary": 1.0,
        "regex": 1.0,
        "ner_model": 0.8,
        "llm": 0.7,
    }

    def calculate_fact_confidence(
        self,
        extraction_method: str,
        source_type: str,
        supporting_sources_count: int = 0,
        is_expert_verified: bool = False,
        custom_extraction_score: Optional[float] = None
    ) -> ConfidenceResult:
        """
        Calculates confidence score for a fact based on the formula:
        score = (0.35 * ext) + (0.25 * src) + (0.20 * supp) + (0.20 * exp)
        """
        # 1. Extraction Score
        ext_score = custom_extraction_score if custom_extraction_score is not None else \
                    self.EXTRACTION_SCORES.get(extraction_method, 0.5)

        # 2. Source Reliability
        src_score = self.SOURCE_RELIABILITY.get(source_type, 0.5)

        # 3. Supporting Sources Score (Simple linear mapping for MVP)
        # 0 sources -> 0.0, 1 -> 0.33, 2 -> 0.67, 3+ -> 1.0
        if supporting_sources_count >= 3:
            supp_score = 1.0
        else:
            supp_score = supporting_sources_count * 0.33333333

        # 4. Expert Verification Score
        exp_score = 1.0 if is_expert_verified else 0.0

        # Final weighted sum
        final_score = (
            (self.WEIGHT_EXTRACTION * ext_score) +
            (self.WEIGHT_SOURCE * src_score) +
            (self.WEIGHT_SUPPORTING * supp_score) +
            (self.WEIGHT_EXPERT * exp_score)
        )

        # Apply LLM Cap
        llm_cap_applied = False
        if extraction_method == "llm" and not is_expert_verified:
            if final_score > self.LLM_CONFIDENCE_CAP:
                final_score = self.LLM_CONFIDENCE_CAP
                llm_cap_applied = True

        # Round to 3 decimal places for consistency with DB NUMERIC(4,3)
        final_score = round(final_score, 3)

        breakdown = ConfidenceBreakdown(
            extraction_score=ext_score,
            source_reliability=src_score,
            supporting_sources_score=supp_score,
            expert_verification_score=exp_score,
            llm_cap_applied=llm_cap_applied
        )

        explanation = self._generate_explanation(
            extraction_method, source_type, supporting_sources_count,
            is_expert_verified, llm_cap_applied
        )

        return ConfidenceResult(
            score=final_score,
            breakdown=breakdown,
            explanation=explanation
        )

    def _generate_explanation(
        self, method: str, source: str, supp_count: int, verified: bool, capped: bool
    ) -> str:
        parts = [f"Extracted via {method}", f"Source type: {source}"]
        if supp_count > 0:
            parts.append(f"Supported by {supp_count} sources")
        if verified:
            parts.append("Expert verified")
        if capped:
            parts.append("Capped due to LLM-only extraction")

        return "; ".join(parts)
