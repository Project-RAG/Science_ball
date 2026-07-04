import logging
import re
from typing import List, Optional

from app.search.search_service import SearchService
from app.services.llm.llm_gateway import llm_gateway
from app.schemas.llm import LLMRequest, LLMMessage
from app.services.answers.prompt_builder import PromptBuilder
from app.schemas.answers import (
    AnswerRequest,
    AnswerResponse,
    AnswerSummary,
    Citation
)
from app.schemas.search import EvidenceItem

logger = logging.getLogger(__name__)

class AnswerService:
    """
    Orchestrates the synthesis of a grounded answer based on retrieved evidence.
    """

    def __init__(self, search_service: SearchService):
        self.search_service = search_service

    async def synthesize_answer(
        self,
        request: AnswerRequest,
        allowed_access_levels: List[str]
    ) -> AnswerResponse:
        """
        Pipeline: Retrieval -> Grounded Prompting -> LLM Generation -> Synthesis.
        """
        # 1. Retrieve evidence using existing SearchService
        # We wrap the AnswerRequest into a SearchRequest for the search service
        from app.schemas.search import SearchRequest
        search_request = SearchRequest(query=request.query, filters=request.filters)
        search_response = await self.search_service.search(search_request, allowed_access_levels)

        evidence = search_response.results

        if not evidence:
            return self._create_no_evidence_response()

        # 2. Build the grounded prompt
        system_prompt, user_prompt = PromptBuilder.build_synthesis_prompt(
            request.query,
            evidence
        )

        # 3. Generate response via LLMGateway
        llm_request = LLMRequest(
            messages=[
                LLMMessage(role="system", content=system_prompt),
                LLMMessage(role="user", content=user_prompt),
            ],
            temperature=0.1, # Lower temperature for higher grounding/consistency
        )

        try:
            llm_response = await llm_gateway.generate(llm_request)
            text = llm_response.text
        except Exception as e:
            logger.error(f"LLM generation failed during answer synthesis: {str(e)}")
            return self._create_error_response(str(e))

        # 4. Synthesize the final response object
        return self._assemble_response(text, evidence)

    def _assemble_response(self, text: str, all_evidence: List[EvidenceItem]) -> AnswerResponse:
        """
        Parses the LLM output to identify used evidence and extract structured info.
        """
        # Extract citations [ID: ...] from text
        citation_ids = re.findall(r"\[([^\]]+)\]", text)

        used_evidence = []
        citations = []
        for cid in citation_ids:
            # Find the evidence item matching this ID
            match = next((item for item in all_evidence if item.chunk_id == cid), None)
            if match:
                used_evidence.append(match)
                citations.append(Citation(
                    source_id=cid,
                    document_title=match.metadata.title
                ))

        # In a full implementation, we would use the LLM to structuredly return
        # contradictions and gaps. For MVP, we treat them as part of the summary text
        # unless they are explicitly separated by headers in the response.

        # Heuristic for splitting Summary / Contradictions / Gaps if provided by LLM
        summary = text
        contradictions = []
        knowledge_gaps = []

        if "Contradictions:" in text:
            parts = text.split("Contradictions:")
            summary = parts[0].strip()
            rem = parts[1]
            if "Knowledge Gaps:" in rem:
                contradictions_text = rem.split("Knowledge Gaps:")[0].strip()
                knowledge_gaps_text = rem.split("Knowledge Gaps:")[1].strip()
                contradictions = [c.strip() for c in contradictions_text.split("\n") if c.strip()]
                knowledge_gaps = [g.strip() for g in knowledge_gaps_text.split("\n") if g.strip()]
            else:
                contradictions = [c.strip() for c in rem.split("\n") if c.strip()]

        elif "Knowledge Gaps:" in text:
            parts = text.split("Knowledge Gaps:")
            summary = parts[0].strip()
            knowledge_gaps = [g.strip() for g in parts[1].split("\n") if g.strip()]

        return AnswerResponse(
            answer=AnswerSummary(
                summary=summary,
                confidence=0.8 # Proxy confidence; would be calculated based on evidence overlap
            ),
            evidence=used_evidence,
            contradictions=contradictions,
            knowledge_gaps=knowledge_gaps,
            sources=citations
        )

    def _create_no_evidence_response(self) -> AnswerResponse:
        return AnswerResponse(
            answer=AnswerSummary(
                summary="No relevant evidence was found in the knowledge base to answer this query.",
                confidence=0.0
            ),
            evidence=[],
            contradictions=[],
            knowledge_gaps=["The requested information is not present in any indexed documents."],
            sources=[]
        )

    def _create_error_response(self, error_msg: str) -> AnswerResponse:
        return AnswerResponse(
            answer=AnswerSummary(
                summary=f"An error occurred during answer synthesis: {error_msg}",
                confidence=0.0
            ),
            evidence=[],
            contradictions=[],
            knowledge_gaps=[],
            sources=[]
        )
