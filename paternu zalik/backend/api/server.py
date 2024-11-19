from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.responses import FileResponse
from fastapi import Request

from backend.api.routes import router as main_router
from backend.db.database import db, Base


def app_factory(lifespan):
    """Application Factory"""
    app = FastAPI(title="Movies API", lifespan=lifespan)
    
    app.include_router(main_router)
    app.mount("/static", StaticFiles(directory="backend/static"), name="static")
    
    @app.get("/")
    async def read_root():
        return FileResponse("backend/static/index.html")
    
    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await db.create_database()
        async with db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
    finally:
        await db.close()


app = app_factory(lifespan=lifespan)
