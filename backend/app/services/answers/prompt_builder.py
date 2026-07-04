from typing import List
from app.schemas.search import EvidenceItem

class PromptBuilder:
    """
    Builds grounded prompts for LLM synthesis to prevent hallucinations.
    """

    SYSTEM_PROMPT = (
        "You are an expert R&D scientific assistant specializing in mining and metallurgy. "
        "Your goal is to synthesize a concise, accurate answer based ONLY on the provided evidence. "
        "\n\nStrict Constraints:\n"
        "1. USE ONLY THE PROVIDED CONTEXT. Do not use external knowledge or invent facts.\n"
        "2. If the evidence does not contain enough information to answer the query, "
        "clearly state that the available documentation is insufficient to provide a complete answer.\n"
        "3. Every technical claim MUST be followed by a citation in the format [source_id].\n"
        "4. Identify and explicitly list any contradictions between different sources found in the evidence.\n"
        "5. Identify any knowledge gaps (specific parts of the query that cannot be answered with the provided context).\n"
        "6. Maintain a professional, objective, and scientific tone."
    )

    @staticmethod
    def build_evidence_block(evidence: List[EvidenceItem]) -> str:
        """Formats evidence items into a structured block for the LLM."""
        if not evidence:
            return "No evidence available."

        blocks = []
        for item in evidence:
            # Using [ID: chunk_id] (Doc: title) Text format as per plan
            block = f"[ID: {item.chunk_id}] (Doc: {item.metadata.title}) {item.text}"
            blocks.append(block)

        return "\n\n".join(blocks)

    @classmethod
    def build_synthesis_prompt(cls, query: str, evidence: List[EvidenceItem]) -> tuple[str, str]:
        """
        Returns (system_prompt, user_prompt).
        """
        evidence_text = cls.build_evidence_block(evidence)

        user_prompt = (
            f"Evidence:\n{evidence_text}\n\n"
            f"Query: {query}\n\n"
            "Please provide a synthesized answer with citations, "
            "list any contradictions found, and identify knowledge gaps."
        )

        return cls.SYSTEM_PROMPT, user_prompt
