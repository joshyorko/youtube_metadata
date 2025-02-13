# YouTube Automation Tools

![Logo](logo.jpg)

This project provides a scaffold for a FastAPI microservice designed for YouTube content automation. It includes four key services: a transcribe service, a thumbnail creation service, a metadata service, and an upload service.

## Services

1. **Transcribe Service:** Translates audio tracks from videos into text.
2. **Thumbnail Creation Service:** Automates the generation of video thumbnails.
3. **Metadata Service:** Handles video metadata, including titles, descriptions, and tags.
4. **Upload Service:** Automates the uploading of videos to YouTube, integrating YouTube's API for video uploads.

## Setup

WORK IN PROGRESS

## Authentication

The `/transcribe` endpoint is secured with JWT-based authentication. You need to obtain a JWT token to access this endpoint.

### Steps to Obtain a JWT Token

1. **Obtain a Token:**
   - Send a POST request to the `/auth/token` endpoint with your username and password.
   - Example using `curl`:
     ```sh
     curl -X POST "http://localhost:8000/auth/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=johndoe&password=secret"
     ```
   - The response will contain the JWT token.

2. **Use the Token:**
   - Include the token in the `Authorization` header of your requests to the `/transcribe` endpoint.
   - Example using `curl`:
     ```sh
     curl -X POST "http://localhost:8000/transcribe" -H "Authorization: Bearer YOUR_TOKEN" -F "file=@path/to/your/file"
     ```

### Environment Variables

Ensure the following environment variables are set:

- `SECRET_KEY`: A secret key for signing JWT tokens.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes.

### Token Refresh

If long-lived sessions are required, you can use the `/auth/refresh` endpoint to obtain a new token.

### Error Handling

The API will return appropriate error responses for issues such as token expiration or malformed tokens. Ensure to handle these errors in your client application.

### Integration Tests

Automated tests are included to verify both valid and invalid authentication scenarios. Refer to the `tests` directory for more details.
