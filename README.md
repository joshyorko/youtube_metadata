# YouTube Automation Tools

![Logo](logo.jpg)

This project provides a scaffold for a FastAPI microservice designed for YouTube content automation. It includes four key services: a transcribe service, a thumbnail creation service, a metadata service, and an upload service.

## Services

1. **Transcribe Service:** Translates audio tracks from videos into text.
2. **Thumbnail Creation Service:** Automates the generation of video thumbnails.
3. **Metadata Service:** Handles video metadata, including titles, descriptions, and tags.
4. **Upload Service:** Automates the uploading of videos to YouTube, integrating YouTube's API for video uploads.

## Setup

### Prerequisites

- Docker
- Docker Compose
- Python 3.9+
- FastAPI
- Uvicorn

### Running the Services

1. Clone the repository:
   ```sh
   git clone https://github.com/joshyorko/youtube_metadata.git
   cd youtube_metadata
   ```

2. Build and start the services using Docker Compose:
   ```sh
   docker-compose up --build
   ```

3. The services will be available at the following endpoints:
   - Transcribe Service: `http://localhost:8000`
   - Thumbnail Creation Service: `http://localhost:8001`
   - Metadata Service: `http://localhost:8002`
   - Upload Service: `http://localhost:8003`

### Running the CI/CD Pipeline

1. Ensure you have the necessary environment variables set up for the CI/CD pipeline.

2. Trigger the pipeline using your preferred CI/CD tool (e.g., GitHub Actions, GitLab CI, Jenkins).

3. The pipeline will include steps for testing, linting, and building container images.

## GitOps Best Practices and Deployment Strategies

### GitOps Principles

- **Declarative Configuration:** Use declarative configuration files to define the desired state of your application and infrastructure.
- **Version Control:** Store all configuration files in a version control system (e.g., Git) to track changes and enable rollbacks.
- **Automated Deployments:** Use automation tools to apply configuration changes and deploy applications consistently.

### Deployment Strategies

- **Continuous Deployment:** Automatically deploy changes to the production environment after passing all tests and quality checks.
- **Blue-Green Deployment:** Maintain two identical environments (blue and green) and switch traffic between them to minimize downtime during deployments.
- **Canary Releases:** Gradually roll out changes to a small subset of users before deploying to the entire user base.

### Tools and Technologies

- **Argo CD:** A GitOps continuous delivery tool for Kubernetes.
- **Flux:** A set of continuous and progressive delivery solutions for Kubernetes.
- **Helm:** A package manager for Kubernetes that helps define, install, and upgrade applications.
