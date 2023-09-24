from fastapi import Request, HTTPException

from app.services.authentication import login_required
from app.models import Object


@login_required
async def get_object(request: Request, object_id: str, watch_id: str):
    object_instance = await Object.get_or_none(id=object_id, watch__user=request.user, watch_id=watch_id)
    if object_instance is None:
        raise HTTPException(
            detail=f"Object {object_id} for user {request.user} is not found.",
            status_code=404
        )
    return object_instance
