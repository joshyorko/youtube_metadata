import requests

# Define the API URL and the YouTube URL
api_url = "http://localhost:8000/"  # Adjust this to your deployed FastAPI endpoint
youtube_url = "https://www.youtube.com/watch?v=az81MHug0Nw"

# Create the payload with the YouTube URL
payload = {
    'youtube_url': youtube_url
}

# Send the POST request
response = requests.post(api_url, params=payload)

# Check if the request was successful
if response.status_code == 200:
    transcription_result = response.json()
    print("Transcription Result:", transcription_result)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
