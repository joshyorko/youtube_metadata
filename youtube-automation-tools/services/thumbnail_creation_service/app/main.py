from fastapi import FastAPI
from .routes import router as thumbnail_router
import asyncio

app = FastAPI(title="Thumbnail Creation Service")

app.include_router(thumbnail_router)

@app.get("/health-check/")
async def health_check():
    return {"message": "Service is operational"}

@app.on_event("startup")
async def startup_event():
    task = asyncio.create_task(health_check_background())
    if not task.done():
        print("Health check background task started")

async def health_check_background():
    while True:
        print("Health check: Service is operational")
        await asyncio.sleep(60)
