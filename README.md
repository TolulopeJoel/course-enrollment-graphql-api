# E-Learning Platform Documentation

## Project Overview

This project is a microservices-based online learning platform that consists of four main services:

1. Gateway Service
2. User Management Service
3. Course Management Service
4. Enrollments Management Service

The platform uses GraphQL for API communication and is containerized using Docker. It's designed to be deployed on Kubernetes.

## Architecture

The system follows a microservices architecture with the following components:

- **Gateway**: Acts as the entry point for all client requests, routing them to appropriate services.
- **User Management**: Handles user-related operations like authentication and user information.
- **Course Management**: Manages course-related operations.
- **Enrollments Management**: Handles course enrollment operations.

## Services

### 1. Gateway Service

The Gateway service is built using FastAPI and Strawberry GraphQL. It acts as an API Gateway, routing requests to the appropriate microservices.

Key features:
- Aggregates GraphQL schemas from other services
- Handles authentication token verification
- Provides a single endpoint for client applications

File: `gateway/gateway.py`
```python:gateway/gateway.py
startLine: 1
endLine: 43
```

### 2. User Management Service

The User Management service is built with Django and Graphene-Django. It handles user-related operations.

Key features:
- User registration
- Authentication (JWT-based)
- User profile management

File: `user_management_service/apps/accounts/schema.py`
```python:user_management_service/apps/accounts/schema.py
startLine: 1
endLine: 61
```

### 3. Course Management Service

The Course Management service is built with Flask, SQLAlchemy, and Graphene. It manages course-related operations.

Key features:
- Course creation
- Course listing
- Course details retrieval

File: `course_management_service/schema.py`
```python:course_management_service/schema.py
startLine: 1
endLine: 58
```

### 4. Enrollments Management Service

The Enrollments Management service is built with Django and Graphene-Django. It handles course enrollment operations.

Key features:
- Course enrollment
- Enrollment listing
- Enrollment verification

File: `enrollments_management_service/enrollments/schema.py`
```python:enrollments_management_service/enrollments/schema.py
startLine: 1
endLine: 42
```

## Database Schema

Each service manages its own database:

1. User Management: Uses Django's default SQLite database
2. Course Management: Uses SQLite with SQLAlchemy ORM
3. Enrollments Management: Uses Django's default SQLite database

## API Documentation

The platform uses GraphQL for API communication. Each service exposes its own GraphQL schema, which is then aggregated by the Gateway service.

### Main Queries

1. `users`: List all users (admin only)
2. `whoami`: Get current user information
3. `allCourses`: List all courses
4. `course(id: ID!)`: Get details of a specific course
5. `enrollments`: List all enrollments (admin only)
6. `enrollment(id: ID!)`: Get details of a specific enrollment

### Main Mutations

1. `createUser(email: String!, password: String!)`: Register a new user
2. `tokenAuth(username: String!, password: String!)`: Authenticate a user and get JWT tokens
3. `refreshToken(refreshToken: String!)`: Refresh an expired JWT token
4. `createCourse(title: String!, description: String!)`: Create a new course
5. `createEnrollment(userId: ID!, courseId: ID!)`: Enroll a user in a course

## Authentication

The platform uses JWT (JSON Web Tokens) for authentication. The User Management service issues and verifies these tokens.

## Deployment

The project is containerized using Docker and can be deployed on Kubernetes.

Docker Compose file for local development:
```yaml:docker-compose.yml
startLine: 1
endLine: 30
```

Kubernetes deployment files are available in the `k8s/` directory.
