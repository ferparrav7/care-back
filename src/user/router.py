import logging
from fastapi import APIRouter, HTTPException, status, Depends
from src.database.postgres import database, user_table
from src.user.model import UserIn
from src.auth.service import get_password_hash, get_user, get_current_user
from typing import Annotated

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", status_code=201)
async def register(user: UserIn):
    if await get_user(str(user.email)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    hashed_password = get_password_hash(user.password)
    query = user_table.insert().values(email=str(user.email), password=hashed_password)

    logger.debug(query)

    await database.execute(query)
    return {"detail": "User created successfully"}


@router.get("/me")
async def me(
        current_user: Annotated[dict, Depends(get_current_user)]
):
    return {
        "email": current_user.email
    }
