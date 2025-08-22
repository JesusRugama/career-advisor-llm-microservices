from fastapi import FastAPI
from domains.prompts import router as prompts_router
from domains.conversations import router as conversations_router
from domains.messages import router as messages_router
from domains.users import router as users_router
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from database import create_tables, close_engine

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    await create_tables()  # Initialize database on startup
    yield
    await close_engine()  # Properly close the database engine

# Include routers from domain structure
app.include_router(conversations_router.router, prefix="/api", tags=["conversations"])
app.include_router(messages_router.router, prefix="/api", tags=["messages"])
app.include_router(users_router.router, prefix="/api", tags=["users"])
app.include_router(prompts_router.router, prefix="/api", tags=["prompts"])

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
