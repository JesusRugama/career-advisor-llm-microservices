from typing import Union
from fastapi import FastAPI
from routers import users, conversations, prompts
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import create_tables

app = FastAPI(title="Career Advisor API", version="1.0.0")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Your list of allowed origins
    allow_credentials=True, # Allow cookies, authorization headers, etc.
    allow_methods=["*"],    # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],    # Allow all headers
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await create_tables()

# Include routers from separate files
app.include_router(conversations.router, prefix="/api", tags=["conversations"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(prompts.router, prefix="/api", tags=["prompts"])

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
