import os
from typing import Union
from fastapi import FastAPI
from dotenv import load_dotenv

app = FastAPI()

# Load .env file
load_dotenv()

@app.get("/")
async def read_root():
    os.getenv("DB_URL")
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}