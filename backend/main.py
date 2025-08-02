from typing import Union
from fastapi import FastAPI
from routers import users, advice
from config import settings

app = FastAPI()

# Include routers from separate files
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(advice.router, prefix="/advice", tags=["advice"])

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}