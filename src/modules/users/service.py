from typing import Optional

from fastapi import HTTPException, status
from sqlmodel import Session

from src.core.security import create_access_token, get_password_hash, verify_password
from src.modules.users.models import User
from src.modules.users.repository import UserRepository
from src.modules.users.schemas import Token, UserCreate, UserUpdate


class UserService:
    def __init__(self, session: Session):
        self.repository = UserRepository(session)

    def authenticate(self, username: str, password: str) -> Optional[User]:
        user = self.repository.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create_user(self, user_create: UserCreate) -> User:
        if self.repository.get_by_email(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        if self.repository.get_by_username(user_create.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
            )

        hashed_password = get_password_hash(user_create.password)
        user = User(
            email=user_create.email,
            username=user_create.username,
            hashed_password=hashed_password,
        )
        return self.repository.create(user)

    def get_user(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        user = self.get_user(user_id)

        update_data = user_update.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )

        if "email" in update_data and update_data["email"] != user.email:
            existing_user = self.repository.get_by_email(update_data["email"])
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

        if "username" in update_data and update_data["username"] != user.username:
            existing_user = self.repository.get_by_username(update_data["username"])
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken",
                )

        for key, value in update_data.items():
            setattr(user, key, value)

        return self.repository.update(user)

    def login(self, username: str, password: str) -> Token:
        user = self.authenticate(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(data={"sub": str(user.id)})
        return Token(access_token=access_token)
