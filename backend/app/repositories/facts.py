"""Repository for persisting numeric conditions and facts."""

from typing import List, Optional, Sequence
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.models.fact import Fact, NumericCondition, FactVersion
from app.models.base import Base


class FactsRepository:
    """
    Handles persistence of numeric conditions and the facts that link them to subjects.
    """

    async def create_numeric_condition(
        self,
        session: AsyncSession,
        data: dict
    ) -> NumericCondition:
        """
        Creates a new numeric condition record.
        Expects data compatible with NumericCondition model.
        """
        condition = NumericCondition(**data)
        session.add(condition)
        await session.flush() # Get the generated ID
        return condition

    async def create_fact(
        self,
        session: AsyncSession,
        data: dict
    ) -> Fact:
        """
        Creates a new fact record.
        Expects data compatible with Fact model.
        """
        fact = Fact(**data)
        session.add(fact)
        await session.flush()
        return fact

    async def create_condition_and_fact(
        self,
        session: AsyncSession,
        subject_id: str,
        subject_type: str,
        condition_data: dict,
        predicate: str = "OPERATES_AT_CONDITION"
    ) -> tuple[NumericCondition, Fact]:
        """
        Atomic operation to create both the condition and the fact linking it.
        """
        # 1. Create the NumericCondition
        condition = await self.create_numeric_condition(session, condition_data)

        # 2. Create the Fact linking the subject to this condition
        fact_data = {
            "subject_id": subject_id,
            "subject_type": subject_type,
            "predicate": predicate,
            "object_id": str(condition.id),
            "object_type": "NumericCondition",
            "extraction_method": "regex",
            "confidence": 1.0, # Deterministic regex is high confidence for MVP
        }
        fact = await self.create_fact(session, fact_data)

        return condition, fact

    async def get_by_document(self, session: AsyncSession, document_id: UUID) -> List[Fact]:
        """Retrieve all facts associated with a specific document."""
        from sqlalchemy import select
        stmt = select(Fact).where(Fact.source_document_id == document_id)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_numeric_conditions_by_document(self, session: AsyncSession, document_id: UUID) -> List[NumericCondition]:
        """Retrieve all numeric conditions associated with a specific document."""
        from sqlalchemy import select
        stmt = select(NumericCondition).where(NumericCondition.source_document_id == document_id)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_pending_reviews(
        self,
        session: AsyncSession,
        document_id: UUID | None = None,
        min_confidence: float | None = None,
        max_confidence: float | None = None
    ) -> List[Fact]:
        """Retrieve facts awaiting human verification."""
        stmt = select(Fact).where(Fact.verification_status == "machine_extracted")

        if document_id:
            stmt = stmt.where(Fact.source_document_id == document_id)
        if min_confidence is not None:
            stmt = stmt.where(Fact.confidence >= min_confidence)
        if max_confidence is not None:
            stmt = stmt.where(Fact.confidence <= max_confidence)

        result = await session.execute(stmt)
        return result.scalars().all()

    async def update_verification_status(
        self,
        session: AsyncSession,
        fact_id: UUID,
        status: str
    ) -> None:
        """Update the verification status of a fact."""
        stmt = (
            update(Fact)
            .where(Fact.id == fact_id)
            .values(verification_status=status)
        )
        await session.execute(stmt)

    async def save_fact_version(
        self,
        session: AsyncSession,
        fact: Fact,
        changed_by: UUID | None = None,
        reason: str | None = None
    ) -> FactVersion:
        """Saves current state of a fact to history before update."""
        # Determine current version number
        from sqlalchemy import func
        version_stmt = select(func.max(FactVersion.version)).where(FactVersion.fact_id == fact.id)
        res = await session.execute(version_stmt)
        current_max = res.scalar() or 0

        # Create payload from current Fact state
        payload = {
            "subject_id": fact.subject_id,
            "subject_type": fact.subject_type,
            "predicate": fact.predicate,
            "object_id": fact.object_id,
            "object_type": fact.object_type,
            "confidence": fact.confidence,
            "verification_status": fact.verification_status,
        }

        version = FactVersion(
            fact_id=fact.id,
            version=current_max + 1,
            payload=payload,
            changed_by=changed_by,
            change_reason=reason
        )
        session.add(version)
        await session.flush()
        return version

    async def get_fact_history(self, session: AsyncSession, fact_id: UUID) -> List[FactVersion]:
        """Retrieve the version history of a specific fact."""
        from sqlalchemy import select
        stmt = select(FactVersion).where(FactVersion.fact_id == fact_id).order_by(FactVersion.version)
        result = await session.execute(stmt)
        return result.scalars().all()

