from fastapi import APIRouter, Query, Depends
from typing import List, Optional
from app.database import books_collection

router = APIRouter()

@router.get("/books", summary="Get available books with filtering & search")
async def get_available_books(
        genre: Optional[str] = Query(None, description="Filter by genre"),
        publisher: Optional[str] = Query(None, description="Filter by publisher"),
        sub_category: Optional[str] = Query(None, description="Filter by sub-category"),
        search: Optional[str] = Query(None, description="Search book titles"),
        limit: int = Query(10, description="Limit number of results", ge=1, le=100),
        skip: int = Query(0, description="Skip number of results", ge=0)
):
    """Fetches available books with filters & search."""

    query = {"is_available": True} # make sure only available books are shown

    if genre:
        query["genre"] = genre
    if publisher:
        query["publisher"] = publisher
    if sub_category:
        query["sub_category"] = sub_category

    if search:
        query["title"] = {"$regex": search, "$options": "i"}

    books_cursor = books_collection.find(query).skip(skip).limit(limit)
    books_list = await books_cursor.to_list(length=limit)

    return {"count": len(books_list), "books": books_list}