from fastapi import APIRouter, Query, Depends, HTTPException
from bson import ObjectId
from typing import List, Optional
from database import books_collection

router = APIRouter()

@router.get("/books", summary="Get available books with filtering & search")
async def get_available_books(
        genre: Optional[str] = Query(None, description="Filter by genre"),
        publisher: Optional[str] = Query(None, description="Filter by publisher"),
        sub_category: Optional[str] = Query(None, description="Filter by sub-category"),
        search: Optional[str] = Query(None, description="Search book titles"),
        limit: int = Query(10, description="Limit number of results", ge=1, le=100),
        skip: int = Query(0, description="Skip number of results", ge=0),
):
    """Fetch available books with filters & search using MongoDB aggregation."""

    match_stage = {"$match": {"is_available": True}}  # Ensure only available books are shown

    # Add filters dynamically
    if genre:
        match_stage["$match"]["genre"] = genre
    if publisher:
        match_stage["$match"]["publisher"] = publisher
    if sub_category:
        match_stage["$match"]["sub_category"] = sub_category
    if search:
        match_stage["$match"]["title"] = {"$regex": search, "$options": "i"}

    pipeline = [
        match_stage,
        {"$project": {
            "id": {"$toString": "$_id"},
            "_id": 0,
            "title": 1,
            "genre": 1,
            "publisher": 1,
            "sub_category": 1,
            "cover_image": 1,
            "author": 1,
            "publication_date": 1,
            "isbn": 1,
            "is_available": 1,
            "language": 1,
            "file": 1,
            "producer_id":1
        }},
        {"$skip": skip},
        {"$limit": limit}
    ]

    books_cursor = books_collection.aggregate(pipeline)
    books_list = await books_cursor.to_list(length=limit)

    return {"count": len(books_list), "books": books_list}


@router.get("/books/{book_id}", summary="Get a single book by ID")
async def get_book(book_id: str):
    """Fetch a single book by ID using MongoDB aggregation."""

    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID format")

    pipeline = [
        {"$match": {"_id": ObjectId(book_id)}},  # Match book by ID
        {"$project": {
            "id": {"$toString": "$_id"},
            "_id": 0,
            "title": 1,
            "genre": 1,
            "publisher": 1,
            "sub_category": 1,
            "is_available": 1,
            "author": 1,
            "publication_date": 1,
            "isbn": 1,
            "language": 1,
            "file": 1,
            "cover_image": 1,
        }}
    ]
    books_cursor = books_collection.aggregate(pipeline)
    book = await books_cursor.to_list(length=1)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book[0]