from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
def get_users():
    return {
        "status": "ok",
        "message": "Users fetched successfully",
    }
