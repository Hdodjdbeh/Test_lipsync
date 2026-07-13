from fastapi import FastAPI

from app.api.routes import router
from app.db.database import Base
from app.db.database import engine

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Avatar Service",
    version="1.0.0",
)

app.include_router(router)