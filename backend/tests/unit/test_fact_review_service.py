import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.review.fact_review_service import FactReviewService
from app.repositories.facts import FactsRepository
from app.repositories.audit_logs import AuditLogRepository
from app.models.fact import Fact

@pytest.fixture
def mock_facts_repo():
    return MagicMock(spec=FactsRepository)

@pytest.fixture
def mock_audit_repo():
    return MagicMock(spec=AuditLogRepository)

@pytest.fixture
def mock_session():
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
def service(mock_facts_repo, mock_audit_repo):
    return FactReviewService(mock_facts_repo, mock_audit_repo)

@pytest.mark.asyncio
async def test_verify_fact_success(service, mock_facts_repo, mock_audit_repo, mock_session):
    fact_id = uuid4()
    user_id = uuid4()

    await service.verify_fact(mock_session, fact_id, user_id, "Looks good")

    mock_facts_repo.update_verification_status.assert_called_once_with(
        mock_session, fact_id, "expert_verified"
    )
    mock_audit_repo.create.assert_called_once()
    args = mock_audit_repo.create.call_args[1]
    assert args["action"] == "fact_verify"
    assert args["entity_id"] == str(fact_id)
    assert args["payload"] == {"comment": "Looks good"}

@pytest.mark.asyncio
async def test_reject_fact_success(service, mock_facts_repo, mock_audit_repo, mock_session):
    fact_id = uuid4()
    user_id = uuid4()

    await service.reject_fact(mock_session, fact_id, user_id, "Incorrect value")

    mock_facts_repo.update_verification_status.assert_called_once_with(
        mock_session, fact_id, "rejected"
    )
    mock_audit_repo.create.assert_called_once()
    args = mock_audit_repo.create.call_args[1]
    assert args["action"] == "fact_reject"
    assert args["payload"] == {"reason": "Incorrect value"}

@pytest.mark.asyncio
async def test_edit_and_verify_fact_success(service, mock_facts_repo, mock_audit_repo, mock_session):
    fact_id = uuid4()
    user_id = uuid4()
    updates = {"confidence": 0.95, "predicate": "NEW_PREDICATE"}

    # Mock the fact object
    mock_fact = MagicMock(spec=Fact)
    mock_fact.id = fact_id
    mock_fact.confidence = 0.7
    mock_fact.predicate = "OLD_PREDICATE"
    mock_fact.verification_status = "machine_extracted"

    # Mock the session execute for fetching the fact
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_fact
    mock_session.execute.return_value = mock_result

    await service.edit_and_verify_fact(mock_session, fact_id, user_id, updates, "Updating based on new study")

    # Check if version was saved first
    mock_facts_repo.save_fact_version.assert_called_once()

    # Check if values were updated on the object
    assert mock_fact.confidence == 0.95
    assert mock_fact.predicate == "NEW_PREDICATE"
    assert mock_fact.verification_status == "expert_verified"

    # Check audit log
    mock_audit_repo.create.assert_called_once()
    args = mock_audit_repo.create.call_args[1]
    assert args["action"] == "fact_edit_verify"
    assert args["payload"]["updates"] == updates
