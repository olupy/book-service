from fastapi import FastAPI
from app.api.routes.auth_routes import router as auth_router
from app.api.routes.books import router as book
import asyncio
from app.consumer import consume_books, start_kafka_consumer
from contextlib import asynccontextmanager
app = FastAPI(title="FastAPI Library Service")

app.include_router(auth_router)
app.include_router(book)

@app.on_event("startup")
def start_consumer():
    """Start the consumer"""
    start_kafka_consumer()

@app.get("/")
async def root():
    return {"message": "book service is running"}
