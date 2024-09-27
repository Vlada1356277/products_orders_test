from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import Session

from config import settings
from database.database import SessionLocal
from routers import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    db: Session = SessionLocal()
    yield
    db.close()

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)



if __name__ == '__main__':
    uvicorn.run("main:app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True)
