# YouTube Automation Tools

![Logo](logo.jpg)

This project provides a scaffold for a FastAPI microservice designed for YouTube content automation. It includes four key services: a transcribe service, a thumbnail creation service, a metadata service, and an upload service.

## Services

1. **Transcribe Service:** Translates audio tracks from videos into text.
2. **Thumbnail Creation Service:** Automates the generation of video thumbnails.
3. **Metadata Service:** Handles video metadata, including titles, descriptions, and tags.
4. **Upload Service:** Automates the uploading of videos to YouTube, integrating YouTube's API for video uploads.

## Setup

Ensure Docker and Docker Compose are installed on your machine. Then, navigate to the project root directory and run the following command to start the services:

```bash
docker-compose up
```

## API Documentation

Each service provides its own API documentation using FastAPI’s built-in tools. After starting the services, you can access the documentation at the `/docs` endpoint of each service (e.g., `http://localhost:<service_port>/docs`).

## Error Handling and Logging

Each service includes robust error handling and logging mechanisms to ensure smooth operation and easy debugging.

## Security Features

The project prioritizes security features, such as API rate limiting and secure API keys management, especially for the YouTube upload service.

## Scalability

The services are designed for scalability to accommodate varying load levels.

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.