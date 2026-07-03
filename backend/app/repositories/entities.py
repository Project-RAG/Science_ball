from typing import Sequence, List, Dict, Any
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entity import Entity


class EntitiesRepository:
    """Repository for managing extracted entities."""

    async def create(self, session: AsyncSession, entity_data: dict) -> Entity:
        """Persist a single entity."""
        entity = Entity(**entity_data)
        session.add(entity)
        await session.flush()
        return entity

    async def create_many(self, session: AsyncSession, entities_data: List[dict]) -> None:
        """Bulk insert entities for efficiency."""
        entities = [Entity(**data) for data in entities_data]
        session.add_all(entities)
        await session.flush()

    async def get_by_document(self, session: AsyncSession, document_id: UUID) -> Sequence[Entity]:
        """Retrieve all entities extracted from a specific document."""
        query = select(Entity).where(Entity.document_id == document_id)
        result = await session.execute(query)
        return result.scalars().all()

    async def delete_by_document(self, session: AsyncSession, document_id: UUID) -> None:
        """Remove all entities associated with a document (for re-processing)."""
        from sqlalchemy import delete
        stmt = delete(Entity).where(Entity.document_id == document_id)
        await session.execute(stmt)
