from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from db.init_db import init_db

from api.user import router as user_router

app = FastAPI()

origins = os.getenv("CORS_ORIGINS", "").split(",") if os.getenv("CORS_ORIGINS") else ["http://localhost:5173"]
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

@app.on_event("startup")
async def on_startup():
    await init_db()
    
app.include_router(user_router) 
