from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_users():
    return {"message": "List of users from DB"}

@router.post("/")
async def create_user():
    return {"message": "User created"}