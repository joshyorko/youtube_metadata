import os
import asyncio
import logging
from openai import AsyncOpenAI
from ..schemas import ThumbnailResponse, ImageData  # Adjust import path as necessary
from ..config import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load settings and create an AsyncOpenAI client instance
settings = Settings()
client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY", settings.openai_api_key))

# Asynchronous function to generate a thumbnail image
async def generate_thumbnail(description: str) -> ThumbnailResponse:
    # Log the start of the thumbnail generation
    logger.info(f"Starting thumbnail generation for description: '{description}'")

    try:
        # Generate an image based on the provided description using the AsyncOpenAI client.
        response = await client.images.generate(
            model="dall-e-3",  # Model used for generating the image
            prompt=description,  # Description to generate the image from
            size="1024x1024",  # Size of the generated image
            quality="standard",  # Quality setting for the image
            style="vivid",  # Style setting for the image
        )
        logger.info("Image generation request completed.")
        logger.info(f"Response: {response}")
    except Exception as e:
        # Log and re-raise any errors encountered during the image generation request
        logger.error(f"Error during image generation request: {e}")
        raise

    # Check if the response contains image data
    try:
        if len(response.data) > 0:
            logger.info("Image data found in response.")
            # Extract image data from the response and create a list of ImageData objects
            image_data_list = [
                ImageData(
                    b64_json=getattr(item, "b64_json", None),  # Base64 encoded image data
                    revised_prompt=getattr(item, "revised_prompt", ""),  # Revised prompt, if available
                    url=getattr(item, "url", ""),  # URL to the generated image
                )
                for item in response.data
            ]

            # Get the creation timestamp from the response
            created = getattr(response, "created", 0)
            logger.info(f"Thumbnail generated successfully with creation timestamp: {created}")

            # Return the ThumbnailResponse object containing the image data
            return ThumbnailResponse(created=created, data=image_data_list)
    except AttributeError:
        # Handle cases where response does not have 'data' attribute
        logger.error(f"No image data returned from the API response for description: '{description}'")
        raise ValueError(f"Failed to generate thumbnail for description: '{description}'. No image data returned.")