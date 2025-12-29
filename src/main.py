import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database.postgres import database
# from storeapi.logging_conf import configure_logging
from src.files.router import router as upload_router
from src.user.router import router as user_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
#app.add_middleware(CorrelationIdMiddleware)
app.include_router(upload_router)
app.include_router(user_router)
