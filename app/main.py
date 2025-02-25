from fastapi import FastAPI
from api.routes.auth_routes import router as auth_router
from api.routes.books import router as book
from api.routes.borrow import router as borrow
import asyncio
from consumer import consume_books, start_kafka_consumer
from contextlib import asynccontextmanager
app = FastAPI(title="FastAPI Library Service")

app.include_router(auth_router)
app.include_router(book)
app.include_router(borrow)

@app.on_event("startup")
def start_consumer():
    """Start the consumer"""
    start_kafka_consumer()

@app.get("/")
async def root():
    return {"message": "book service is running"}
