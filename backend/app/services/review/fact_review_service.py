"""Service for managing the human-in-the-loop review process of facts."""

from __future__ import annotations

import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.facts import FactsRepository
from app.repositories.audit_logs import AuditLogRepository
from app.models.fact import Fact
from app.schemas.facts import FactDetailResponse

class FactReviewService:
    def __init__(self, facts_repo: FactsRepository, audit_repo: AuditLogRepository):
        self.facts_repo = facts_repo
        self.audit_repo = audit_repo

    async def list_pending_facts(
        self,
        session: AsyncSession,
        document_id: uuid.UUID | None = None,
        min_confidence: float | None = None,
        max_confidence: float | None = None
    ) -> List[Fact]:
        """Returns facts awaiting verification."""
        return await self.facts_repo.get_pending_reviews(
            session, document_id, min_confidence, max_confidence
        )

    async def verify_fact(
        self,
        session: AsyncSession,
        fact_id: uuid.UUID,
        user_id: uuid.UUID | None,
        comment: Optional[str] = None
    ) -> None:
        """Marks a fact as expert verified."""
        await self.facts_repo.update_verification_status(session, fact_id, "expert_verified")

        await self.audit_repo.create(
            session=session,
            user_id=user_id,
            action="fact_verify",
            entity_type="Fact",
            entity_id=str(fact_id),
            payload={"comment": comment}
        )

    async def reject_fact(
        self,
        session: AsyncSession,
        fact_id: uuid.UUID,
        user_id: uuid.UUID | None,
        reason: str
    ) -> None:
        """Marks a fact as rejected."""
        await self.facts_repo.update_verification_status(session, fact_id, "rejected")

        await self.audit_repo.create(
            session=session,
            user_id=user_id,
            action="fact_reject",
            entity_type="Fact",
            entity_id=str(fact_id),
            payload={"reason": reason}
        )

    async def edit_and_verify_fact(
        self,
        session: AsyncSession,
        fact_id: uuid.UUID,
        user_id: uuid.UUID | None,
        updates: dict,
        comment: Optional[str] = None
    ) -> None:
        """Saves current state to history and updates fact values."""
        # 1. Fetch existing fact
        from sqlalchemy import select
        stmt = select(Fact).where(Fact.id == fact_id)
        result = await session.execute(stmt)
        fact = result.scalar_one_or_none()

        if not fact:
            raise ValueError(f"Fact {fact_id} not found")

        # 2. Archive current state to FactVersion
        await self.facts_repo.save_fact_version(
            session=session,
            fact=fact,
            changed_by=user_id,
            reason=comment or "Fact updated by reviewer"
        )

        # 3. Update fields
        for key, value in updates.items():
            if value is not None and hasattr(fact, key):
                setattr(fact, key, value)

        fact.verification_status = "expert_verified"

        # 4. Audit log
        await self.audit_repo.create(
            session=session,
            user_id=user_id,
            action="fact_edit_verify",
            entity_type="Fact",
            entity_id=str(fact_id),
            payload={"updates": updates, "comment": comment}
        )

    async def add_review_comment(
        self,
        session: AsyncSession,
        fact_id: uuid.UUID,
        user_id: uuid.UUID | None,
        comment: str
    ) -> None:
        """Adds a comment to the audit log without changing status."""
        await self.audit_repo.create(
            session=session,
            user_id=user_id,
            action="fact_comment",
            entity_type="Fact",
            entity_id=str(fact_id),
            payload={"comment": comment}
        )
