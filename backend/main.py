from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

from db.init_db import init_db
from api.user import router as user_router
from api.table import router as table_router
from api.chapters import router as chapters_router
from api.divisions import router as divisions_router
from api.department import router as department_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- Startup: Inicjalizacja bazy danych ---")
    await init_db()
    
    yield  
    
    print("--- Shutdown: Zamykanie aplikacji ---")

app = FastAPI(lifespan=lifespan)

origins_raw = os.getenv("CORS_ORIGINS")
origins = origins_raw.split(",") if origins_raw else ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/test2")
def test2():
    return {"status": "ok"}

app.include_router(user_router) 
app.include_router(table_router)
app.include_router(chapters_router)
app.include_router(divisions_router)
app.include_router(department_router)
