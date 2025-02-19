from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from app.database import users_collection, send_kafka_event
from app.schemas import UserCreate, UserResponse, TokenResponse
from app.auth import hash_password, verify_password, create_jwt_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = {
        "email": user.email, "firstname": user.firstname, "password": hashed_password,"is_active": True,"role": "Client"}
    result = await users_collection.insert_one(new_user)
    kafka_event_data = {
        "id": str(result.inserted_id),
        "email": user.email,
        "firstname": user.firstname,
        "event": "USER_REGISTERED",
        "role": "Client",
        "is_active":  True
    }
    send_kafka_event("user_registration_topic", kafka_event_data)

    return UserResponse(id=str(result.inserted_id), email=user.email, firstname=user.firstname)


@router.post("/login", response_model=TokenResponse)
async def login_user(user: UserCreate):
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {"sub": str(db_user["_id"]), "email": db_user["email"]}
    access_token = create_jwt_token(token_data, timedelta(minutes=60))

    return {"access_token": access_token, "token_type": "bearer"}

