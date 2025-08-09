from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
async def get_users():
    return {"message": "List of users from DB"}

@router.post("/users")
async def create_user():
    return {"message": "User created"}