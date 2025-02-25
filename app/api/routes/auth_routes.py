from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from database import users_collection, send_kafka_event
from schemas import UserCreate, UserResponse, TokenResponse, UserUpdate
from auth import hash_password, verify_password, create_jwt_token
from datetime import timedelta
from typing import Union, List, Optional
from utils import generate_unique_id
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password: str = hash_password(user.password)
    user_id = generate_unique_id()
    new_user: dict[str, Union[str, bool]] = {
        "id":user_id,
        "email": user.email,
        "lastname": user.lastname,
        "firstname": user.firstname,
        "password": hashed_password,
        "is_active": True,
        "role": "Client"
    }
    result = await users_collection.insert_one(new_user)
    inserted_id =  str(result.inserted_id)
    kafka_event_data: dict[str, Union[str, bool]] = {
        "producer_id": inserted_id,
        "email": user.email,
        "firstname": user.firstname,
        "event": "USER_REGISTERED",
        "role": "Client",
        "is_active":  True,
        "lastname": user.lastname,
        "password": hashed_password

    }
    send_kafka_event("user_registration_topic", kafka_event_data) # Send message to subscription that can be consumed

    return UserResponse(id=str(result.inserted_id), email=user.email, firstname=user.firstname)


@router.post("/login", response_model=TokenResponse)
async def login_user(user: UserCreate):
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {"sub": str(db_user["_id"]), "email": db_user["email"]}
    access_token = create_jwt_token(token_data, timedelta(minutes=60))

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users", response_model=List[UserResponse])
async def get_users(
    search: Optional[str] = None,
    is_active: Optional[bool] = None
):
    """Fetch all users."""
    query = {}

    if is_active is not None:
        query["is_active"] = is_active

    if search:
        query["$or"] = [
            {"firstname": {"$regex": search, "$options": "i"}},
            {"lastname": {"$regex": search, "$options": "i"}},
            {"email": {"$regex": search, "$options": "i"}}
        ]

    users = await users_collection.find(query).to_list(length=100)
    return [{**user, "id": str(user["_id"])} for user in users]

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Fetch a single user by ID."""
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {**user, "id": str(user["_id"])}

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_data: UserUpdate):
    """Update user details (only modifiable fields)."""
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    existing_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    updated_fields = {k: v for k, v in user_data.dict(exclude_unset=True).items()}

    if updated_fields:
        await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_fields})

    updated_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    return {**updated_user, "id": str(updated_user["_id"])}

