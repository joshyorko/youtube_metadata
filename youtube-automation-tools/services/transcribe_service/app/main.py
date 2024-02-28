from fastapi import FastAPI
from .routes import transcribe_router
import asyncio

app = FastAPI(title="Transcription Service")

# Include the router from routes.py
app.include_router(transcribe_router, prefix="/transcribe", tags=["Transcription"])




async def health_check():
    while True:
        # Here you can insert real checks, e.g., database connectivity, external API availability, etc.
        print("Health check passed. Application is operational.")
        await asyncio.sleep(60)  # Sleep for 60 seconds before the next check
        
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint.
    Returns a message indicating that the service is running.
    """
    return {"message": "Transcription service is up and running!"}

@app.on_event("startup")
async def start_health_check():
    # Your existing health_check function
    asyncio.create_task(health_check())
