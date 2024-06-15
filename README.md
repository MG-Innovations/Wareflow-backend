### Wareflow Backend: Local Development Setup Guide

The Wareflow backend is a dockerized application that consists of Caddy, PostgreSQL, and FastAPI. This guide will help you set up the backend locally for development purposes.

#### Components Overview

**Caddy**: Caddy is used as a reverse proxy. It allows us to route traffic to different services running on various ports. For example, if our client application (React app) runs on port 3000 and our backend on port 8000, we can configure Caddy to route traffic such that {domain_name}/api directs to localhost:8000 and {domain_name}/client directs to localhost:3000. Alternatives to Caddy include Nginx.

---

### Local Development Setup

#### Pre-requisites

Before cloning the repository, ensure Docker is installed on your local system. Download and install Docker Desktop for [Mac](https://docs.docker.com/desktop/mac/install/) or [Windows](https://docs.docker.com/desktop/windows/install/).

#### Steps to Set Up the Backend Locally

1. **Clone the GitHub Repository**

   Open your terminal and execute the following command:

   ```bash
   git clone https://github.com/MG-Innovations/Wareflow-backend.git
   ```

2. **Navigate to the Project Directory**

   Change your directory to the project folder:

   ```bash
   cd Wareflow-backend
   ```

   **Note**: Ensure Docker Desktop is running. Docker Daemon must be active to execute Docker Compose commands.

3. **Build Docker Images**

   Build the Docker images by running:

   ```bash
   docker-compose build
   ```

4. **Run the Containers**

   Start the containers with:

   ```bash
   docker-compose up
   ```

Following these steps will set up your local environment, allowing you to start development on the Wareflow backend.

---
