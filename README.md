# Authentication Service

This is an authentication service built with FastAPI that provides authentication, OAuth, and password reset functionalities.

## Requirements

- Docker
- Python 3.12+ (for local development)

## Environment Setup

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
SECRET_KEY=your-secret-key
MONGODB_URL=your-mongodb-url
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
```

## Running with Docker

1. Build the Docker image:
```bash
docker build -t auth-service .
```

2. Run the container:
```bash
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name auth-service \
  auth-service
```

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the development server:
```bash
uvicorn main:app --reload
```

## Available Endpoints

### Authentication
- `POST /auth/login` - Login with email and password
- `POST /auth/register` - Register new user

### OAuth
- `GET /auth/google/login` - Start Google login
- `GET /auth/google/callback` - Google login callback

### Password Reset
- `POST /auth/password-reset/request` - Request reset token
- `POST /auth/password-reset/verify` - Verify reset token
- `POST /auth/password-reset/reset` - Reset password

## API Documentation

Access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`