from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from app.database import books_collection, users_collection, borrow_collection
from app.schemas import Borrow
#from app.schemas.book import Book
#from app.schemas.user import User
from app.database import send_kafka_event
from bson import ObjectId
from typing import Any,Optional, List

from common.kgs import generate_unique_id

router = APIRouter()


@router.post("/borrow", summary="Borrow a book")
async def borrow_book(borrow_data: Borrow):
    """Allows a user to borrow a book if it's available."""

    book = await books_collection.find_one({"_id": ObjectId(borrow_data.book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.get("is_available"):
        raise HTTPException(status_code=400, detail="Book is not available for borrowing")

    user = await users_collection.find_one({"_id": ObjectId(borrow_data.user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    borrow_id: str = generate_unique_id()
    borrow_entry = {
        "id":borrow_id,
        "book_id": str(book["_id"]),
        "user_id": str(user["_id"]),
        "borrow_date": borrow_data.borrow_date,
        "return_date": borrow_data.return_date,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "is_active": True,
        "is_returned": False,
        "is_overdue": False,
        "book": book,
        "user": user
    }
    _ = await borrow_collection.insert_one(borrow_entry)
    await books_collection.update_one({"_id": ObjectId(borrow_data.book_id)}, {"$set": {"is_available": False}})
    kafka_event_data: dict[str, Any] = {
        "borrow_id": borrow_id,
        "user_id": borrow_data.user_id,
        "book_id": borrow_data.book_id,
        "borrow_date": borrow_data.borrow_date.isoformat(),
        "return_date": borrow_data.return_date.isoformat(),
        "event": "BOOK_BORROWED"
    }
    send_kafka_event("borrow_book_topic",kafka_event_data)
    return {"message": "Book borrowed successfully", "borrow_id": borrow_id}

@router.get("/borrow", response_model=List[Borrow])
async def get_all_borrows(
        return_date: Optional[datetime] = Query(None, description="Filter by return date"),
        is_returned: Optional[bool] = Query(None, description="Filter by return status"),
        is_overdue: Optional[bool] = Query(None, description="Filter by overdue status"),
        search: Optional[str] = Query(None, description="Search by user/book details")
):
    """Fetch all borrowed books with filters and search capabilities."""
    query = {}
    if return_date:
        query["return_date"] = return_date
    if is_returned is not None:
        query["is_returned"] = is_returned
    if is_overdue is not None:
        query["is_overdue"] = is_overdue
    if search:
        query["$or"] = [
            {"user.firstname": {"$regex": search, "$options": "i"}},  # Case-insensitive
            {"user.lastname": {"$regex": search, "$options": "i"}},
            {"book.title": {"$regex": search, "$options": "i"}},
            {"book.author": {"$regex": search, "$options": "i"}}
        ]

    borrows = await borrow_collection.find(query).to_list(length=100)
    return [{**borrow, "id": str(borrow["_id"])} for borrow in borrows]


@router.get("/borrow/{borrow_id}", response_model=Borrow)
async def get_borrow_by_id(borrow_id: str):
    """Fetch a single borrow record by ID."""
    borrow = await borrow_collection.find_one({"_id": ObjectId(borrow_id)})
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    return {**borrow, "id": str(borrow["_id"])}

@router.get("/borrow/user/{user_id}", response_model=List[Borrow])
async def get_borrows_by_user(user_id: str):
    """Fetch all borrow records for a specific user."""
    borrows = await borrow_collection.find({"user_id": user_id}).to_list(length=100)
    if not borrows:
        raise HTTPException(status_code=404, detail="No borrow records found for this user")
    return [{**borrow, "id": str(borrow["_id"])} for borrow in borrows]
