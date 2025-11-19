from fastapi import APIRouter, status

from src.core.dependencies import CurrentUser, SessionDep
from src.modules.users.schemas import (
    Token,
    UserCreate,
    UserLogin,
    UserPublic,
    UserUpdate,
)
from src.modules.users.service import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED
)
def register(user_create: UserCreate, session: SessionDep):
    service = UserService(session)
    user = service.create_user(user_create)
    return user


@router.post("/login", response_model=Token)
def login(user_login: UserLogin, session: SessionDep):
    service = UserService(session)
    return service.login(user_login.username, user_login.password)


@router.get("/me", response_model=UserPublic)
def get_current_user_info(current_user: CurrentUser):
    return current_user


@router.get("/{user_id}", response_model=UserPublic)
def get_user(user_id: int, session: SessionDep, current_user: CurrentUser):
    service = UserService(session)
    return service.get_user(user_id)


@router.patch("/me", response_model=UserPublic)
def update_current_user(
    user_update: UserUpdate, session: SessionDep, current_user: CurrentUser
):
    service = UserService(session)
    return service.update_user(current_user.id, user_update)
