# Microservice Project - Book Service

## Overview
This project is a microservice-based book service where users can onboard, browse, and borrow books through the main API. An admin API allows administrators to manage book inventory. The services communicate using Kafka for event-driven processing.

- **Main API** (User Service): `http://127.0.0.1:8000/docs`
- **Admin API** (Book Management): `http://127.0.0.1:45000/api/v1/doc`

## Prerequisites
Ensure the following are installed on your system:

- **Python 3.11+**
- **Docker & Docker Compose**
- **Kafka (Managed via Docker Compose)**

## Setup Instructions
### 1. Clone the Project
```sh
git clone <repository-url>
cd <project-folder>
```

### 2. Set Up the Virtual Environment
#### Windows (PowerShell)
```sh
python -m venv venv
venv\Scripts\activate
```
#### macOS/Linux
```sh
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install Poetry:
```sh
pip install poetry
```
Install project dependencies:
```sh
poetry install
```

### 4. Configure Environment Variables
Copy the sample environment file:
```sh
cp .env.sample .env
```

### 5. Run the Services with Docker Compose
```sh
docker compose -f docker-compose.yml up --build
```

## Service Architecture
This project consists of two microservices:

1. **User Service (Main API)**
   - Handles user onboarding and book borrowing.
   - Listens for book availability events from the Admin API via Kafka.
   - Sends events when users borrow books.

2. **Admin Service (Book Management API)**
   - Handles book creation and inventory management.
   - Consumes events from the User Service when a book is borrowed.
   - Produces events notifying book availability status.

## Expanding the Project
This microservice-based architecture can be easily expanded by adding:
- **Notifications Service**: Sends emails or push notifications when book status changes.
- **Payment Service**: Handles late return penalties.
- **Recommendation Engine**: Suggests books based on borrowing history.

## API Documentation
- **User Service (Swagger UI):** `http://127.0.0.1:8000/docs`
- **Admin Service (Swagger UI):** `http://127.0.0.1:45000/api/v1/doc`

## Conclusion
This project demonstrates an event-driven microservice architecture using Kafka for communication. It ensures scalability and decoupling between services, making it easy to extend and integrate new features.

