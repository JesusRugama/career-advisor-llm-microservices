from typing import Union
from fastapi import FastAPI
from routers import users, advice, prompts
from fastapi.middleware.cors import CORSMiddleware
from config import settings

app = FastAPI()

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

# Include routers from separate files
app.include_router(advice.router, prefix="/advice", tags=["advice"])
app.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}