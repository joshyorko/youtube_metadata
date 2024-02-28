from openai import OpenAI
from ..models import ThumbnailResponse, ImageData  # Adjust import path as necessary
import asyncio

# Initialize the OpenAI client with your API key
client = OpenAI()

async def generate_thumbnail(description: str) -> ThumbnailResponse:
    # Generate an image based on the provided description
    response = await asyncio.to_thread(
        client.images.generate,
        model="dall-e-3",
        prompt=description,
        size="1024x1024",
        quality="hd",
        style="natural"
    )
    
    if hasattr(response, 'data') and len(response.data) > 0:
        image_data_list = [ImageData(
            b64_json=getattr(item, 'b64_json', None),
            revised_prompt=getattr(item, 'revised_prompt', ''),
            url=getattr(item, 'url', '')
        ) for item in response.data]
        
        created = getattr(response, 'created', 0)
        
        return ThumbnailResponse(created=created, data=image_data_list)
    else:
        # Handle cases where no image is generated or returned
        raise ValueError("Failed to generate thumbnail. No image data returned.")
