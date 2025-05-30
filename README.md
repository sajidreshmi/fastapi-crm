# FastAPI CRM Backend

A simple CRM backend application built with FastAPI, SQLAlchemy, and SQLite, featuring token-based authentication.

## Features

-   **Customer Management:** Create, Read, Update, and Delete customer records.
-   **User Authentication:** Secure token-based authentication (JWT with OAuth2 Password Flow).
-   **SQLite Database:** Uses SQLite for lightweight and easy-to-set-up data storage.
-   **SQLAlchemy ORM:** Leverages SQLAlchemy for database interactions.
-   **Pydantic Models:** Ensures data validation and serialization.
-   **Modular Structure:** Organized into routers, CRUD operations, models, schemas, and authentication logic.
-   **Basic Error Handling:** Includes custom exception handlers for common errors.
-   **API Versioning:** Implemented URL-based versioning (e.g., `/v1/customers`).
-   **Rate Limiting:** Protects API endpoints using `fastapi-limiter` and Redis.
-   **Health Check Endpoint:** Provides an endpoint to monitor database and Redis connectivity.
-   **Containerization:** Dockerfile and Docker Compose for easy setup and deployment.
-   **Logging:** Basic logging implemented for request and error tracking.
-   **Configuration Management:** Uses `.env` files for managing environment-specific configurations (e.g., database URL, JWT secret).

## Project Structure
