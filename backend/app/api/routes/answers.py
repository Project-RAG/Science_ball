from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.answers import AnswerRequest, AnswerResponse
from app.services.answers.answer_service import AnswerService
from app.search.search_service import SearchService
from app.services.query.query_understanding import QueryUnderstandingService

router = APIRouter()

def get_answer_service(
    search_service: SearchService = Depends(lambda: SearchService(QueryUnderstandingService()))
) -> AnswerService:
    # In a real production setup, we would use a proper dependency injection container
    from app.services.answers.answer_service import AnswerService
    return AnswerService(search_service)

@router.post("/", response_model=AnswerResponse)
async def create_answer(
    request: AnswerRequest,
    service: AnswerService = Depends(get_answer_service)
):
    """
    Generates a grounded answer based on retrieved evidence.
    """
    # Mocking allowed access levels for now (as seen in search route)
    allowed_access_levels = ["public", "internal"]

    try:
        return await service.synthesize_answer(request, allowed_access_levels)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
