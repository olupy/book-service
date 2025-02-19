from fastapi import FastAPI
from app.api.routes.auth_routes import router as auth_router

app = FastAPI(title="FastAPI Library Service")

app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "book service is running"}
