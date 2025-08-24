import sys
import os
# Add shared directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../shared'))
# Add current directory to path for local imports
sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_tables, close_engine
from router import router as messages_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    await create_tables()  # Initialize database on startup
    yield
    await close_engine()  # Properly close the database engine

app = FastAPI(
    title="Messages Service", 
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include messages router (existing code, no modifications)
app.include_router(messages_router, prefix="/api", tags=["messages"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "messages-service"}

@app.get("/")
async def root():
    return {"message": "Messages Service", "version": "1.0.0"}
