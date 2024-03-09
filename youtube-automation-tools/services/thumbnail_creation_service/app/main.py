from fastapi import FastAPI
from .router import router as thumbnail_router
import asyncio

app = FastAPI(title="Thumbnail Creation Service")

app.include_router(thumbnail_router)

@app.get("/health-check/")
async def health_check():
    return {"message": "Service is operational"}

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint.
    Returns a message indicating that the service is running.
    """
    return {"message": "Thumbnail service is up and running!"}


async def health_check_background():
    while True:
        print("Health check: Service is operational")
        await asyncio.sleep(60)
