from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/ping", description="Responds with pong.")
def ping():
    return "pong"
