import logging

from fastapi import APIRouter, HTTPException, status, Depends

from src.database.postgres import database, user_table
from src.user.model import UserIn
from src.auth.service import get_password_hash, get_user, authenticate_user, create_access_token

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", status_code=201)
async def register(user: UserIn):
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    hashed_password = get_password_hash(user.password)
    query = user_table.insert().values(email=user.email, password=hashed_password)

    logger.debug(query)

    await database.execute(query)
    return {"detail": "User created successfully"}
