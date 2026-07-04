from fastapi import APIRouter

from api.schemas.group_schema import (
    GroupSessionCreateRequest,
    GroupSessionFeedbackRequest,
)
from api.services.group_session_service import (
    apply_group_session_feedback,
    create_group_recommendation_session,
    delete_group_recommendation_session,
)


router = APIRouter(
    prefix="/groups",
    tags=["Groups"],
)


@router.post("/session")
def create_group_session(request: GroupSessionCreateRequest):
    return create_group_recommendation_session(
        user_ids=request.user_ids,
        top_k=request.top_k,
        per_user_k=request.per_user_k,
        filters=request.filters,
    )


@router.post("/session/{session_id}/feedback")
def submit_group_session_feedback(
    session_id: str,
    request: GroupSessionFeedbackRequest,
):
    return apply_group_session_feedback(
        session_id=session_id,
        current_restaurant=request.current_restaurant,
        affected_user_ids=request.affected_user_ids,
        reason=request.reason,
        top_k=request.top_k,
        per_user_k=request.per_user_k,
    )

@router.delete("/session/{session_id}")
def delete_group_session(session_id: str):
    return delete_group_recommendation_session(session_id)
