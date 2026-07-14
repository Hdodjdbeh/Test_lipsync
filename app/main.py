from fastapi import FastAPI

from app.api.routes import router
from app.db.database import Base
from app.db.database import engine
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
app = FastAPI(
    title="Avatar Service",
    version="1.0.0",
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)
logger.info("Database initialized")

app.include_router(router)
logger.info("Application started")