from typing import List
from fastapi import FastAPI, HTTPException
from uuid import UUID
from models import User, Gender, Role, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("1ed17aec-a0cf-4a10-a1eb-1c120462fcde"),
        first_name="Jamila",
        last_name="Ahmed",
        gender=Gender.female,
        middle_name="Noah",
        roles=[Role.student, Role.user, Role.admin],
    ),
    User(
        id=UUID("1ed17aec-a0cf-4a10-a1eb-1c120462fcde"),
        first_name="Alex",
        last_name="Jones",
        gender=Gender.female,
        roles=[Role.student],
    ),
]


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id, "message": "User saved successfully"}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    print("passed userid is {}".format(user_id))
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )


@app.put("/api/v1/users/{user_id}",description="update user details")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )
