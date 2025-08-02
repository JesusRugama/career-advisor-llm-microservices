import os
from typing import Union
from fastapi import FastAPI
from dotenv import load_dotenv
from routers import users

app = FastAPI()

# Load .env file
load_dotenv()

app = FastAPI()

# Include routers from separate files
app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}