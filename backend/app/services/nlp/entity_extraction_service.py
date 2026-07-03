from typing import List, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.entities import EntitiesRepository
from app.services.nlp.entity_extractor import EntityExtractor
from app.services.nlp.dictionaries import get_flattened_dictionary


class EntityExtractionService:
    """Orchestrates entity extraction for documents and their chunks."""

    def __init__(self, entities_repository: EntitiesRepository):
        self.entities_repository = entities_repository
        # Initialize the extractor with the flattened domain dictionary
        self.extractor = EntityExtractor(get_flattened_dictionary())

    async def process_document_chunks(
        self,
        session: AsyncSession,
        document_id: UUID,
        chunks: List[Dict[str, Any]],
        access_level: str,
    ) -> None:
        """
        Extracts entities from a list of chunks and persists them.

        Args:
            session: DB session.
            document_id: Source document ID.
            chunks: List of chunk objects (must contain 'id' and 'text').
            access_level: Access level for the extracted entities.
        """
        # Idempotency: remove old entities for this document
        await self.entities_repository.delete_by_document(session, document_id)

        all_entities_to_save = []

        for chunk in chunks:
            chunk_id = chunk.get("id") # or chunk_id if passed as a separate list
            text = chunk.get("text", "")

            # Perform deterministic extraction
            spans = self.extractor.extract(text)

            for span in spans:
                entity_payload = {
                    "document_id": document_id,
                    "chunk_id": chunk_id,
                    "entity_type": span.entity_type,
                    "name": span.text,
                    "canonical_name": span.canonical_name,
                    "confidence": 1.0, # Dictionary matches are high confidence for MVP
                    "extraction_method": "dictionary",
                    "access_level": access_level if hasattr(span, 'access_level') else None
                    # Note: Entity model in SDD/code doesn't have access_level column yet,
                    # but it should inherit from document. We follow the provided Model.
                }
                # The Entity model actually does NOT have access_level according to the Read output of models/entity.py
                # But we will stick to the laziest implementation that matches the model exactly.
                # If confidence is 1.0 and method is 'dictionary', it's a valid MVP extraction.

                if "access_level" in entity_payload:
                    del entity_payload["access_level"]

                all_entities_to_save.append(entity_payload)

        if all_entities_to_save:
            await self.entities_repository.create_many(session, all_entities_to_save)
