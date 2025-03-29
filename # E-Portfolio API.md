# E-Portfolio API

A FastAPI-based backend for managing high school student portfolios. This API provides functionality for student profiles, activities, awards, and skills management with JWT authentication.

## Features

- User authentication with JWT
- Student profile management
- Activity tracking
- Awards and achievements
- Skills assessment
- Timezone-aware timestamps (UTC+7)
- MySQL database integration
- Docker support

## Prerequisites

- Python 3.11+
- MySQL 8.0+
- Docker (optional)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd E_Portfolio/backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```plaintext
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=e_portfolio
SECRET_KEY=your-secret-key
```

To generate a secure SECRET_KEY, run:
```bash
python zero-secret.py
```

## Database Setup

1. Create the database:
```bash
mysql -u root -p
CREATE DATABASE e_portfolio CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Run database migrations:
```bash
alembic upgrade head
```

## Running the Application

### Local Development
```bash
uvicorn main:app --reload
```

### Docker
```bash
docker-compose up --build
```

## API Documentation

Once the application is running, access the interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- POST `/token` - Login and get access token
- POST `/register` - Register new user

### Profile Management
- POST `/profile` - Create student profile
- GET `/profile` - Get current user's profile

### Activities
- POST `/activities` - Create new activity
- GET `/activities` - List user's activities

### Awards
- POST `/awards` - Create new award
- GET `/awards` - List user's awards

### Skills
- POST `/skills` - Create new skill
- GET `/skills` - List available skills
- POST `/student-skills` - Add skill to student profile

## Project Structure
```
backend/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   ├── __init__.py
│   │   └── deps.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   └── session.py
│   ├── models/
│   │   └── models.py
│   └── schemas/
│       └── schemas.py
├── alembic/
├── tests/
├── .env
├── main.py
├── requirements.txt
└── docker-compose.yml
```

## Testing

Run the test suite:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

[MIT License](LICENSE)