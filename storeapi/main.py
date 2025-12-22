import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from storeapi.core.database import database
# from storeapi.logging_conf import configure_logging
from storeapi.routers.upload import router as upload_router
from storeapi.routers.user import router as user_router

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
