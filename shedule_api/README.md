# Weekly Schedule API

A comprehensive Django REST API for managing weekly schedules with time slots and associated IDs. The API includes JWT authentication, comprehensive CRUD operations, and Swagger documentation.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete weekly schedules
- **JWT Authentication**: Secure authentication using djangorestframework-simplejwt
- **Swagger Documentation**: Interactive API documentation
- **User Management**: User registration, login, profile management
- **Time Slot Management**: Flexible time slot configuration for each day of the week
- **Data Validation**: Comprehensive validation for time slots and IDs
- **Soft Delete**: Soft delete functionality for schedules
- **Unit Tests**: Comprehensive test coverage
- **Clean Architecture**: Well-structured Django application with best practices

## Project Structure

```
schedule_api/
├── schedule_api/           # Main project directory
│   ├── __init__.py
│   ├── settings.py        # Django settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py
├── apps/                  # Application modules
│   ├── __init__.py
│   ├── core/             # Core functionality
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── models.py     # Base models
│   │   └── managers.py   # Custom managers
│   ├── schedules/        # Schedule management
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── models.py     # Schedule and TimeSlot models
│   │   ├── serializers.py # API serializers
│   │   ├── views.py      # API views
│   │   ├── urls.py       # URL routing
│   │   └── tests.py      # Unit tests
│   └── authentication/   # User authentication
│       ├── __init__.py
│       ├── admin.py
│       ├── serializers.py # Auth serializers
│       ├── views.py      # Auth views
│       ├── urls.py       # Auth URL routing
│       └── tests.py      # Auth tests
│── templates/   
│   └── swagger/             
│       ├── redoc.html
│       └── swagger-ui.html
├── Dockerfile
├── docker-compose.yml
├── Make
├── requirements.txt       # Python dependencies
├── manage.py             # Django management script
├── .env.example          # Environment variables example
└── README.md             # This file
```

## Installation and Setup

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd schedule_api
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## API Documentation

### Swagger UI
Access the interactive API documentation at: `http://localhost:8000/swagger`

### ReDoc
Alternative documentation format: `http://localhost:8000/redoc/`

## JWT Authentication Implementation

This project uses `djangorestframework-simplejwt` for JWT authentication. Here's how it's implemented:

### 1. Installation and Configuration

```python
# requirements.txt
djangorestframework-simplejwt==5.3.0

# settings.py
INSTALLED_APPS = [
    # ...
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    # ... other settings
}
```

### 2. Authentication Endpoints

- **Register**: `POST /api/v1/auth/register/`
- **Login**: `POST /api/v1/auth/login/`
- **Token Refresh**: `POST /api/v1/auth/token/refresh/`
- **Logout**: `POST /api/v1/auth/logout/`
- **Profile**: `GET/PUT/PATCH /api/v1/auth/profile/`
- **Change Password**: `POST /api/v1/auth/change-password/`

### 3. Usage Examples

#### Registration
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "newuser",
    "email": "user@example.com",
    "first_name": "",
    "last_name": "",
    "is_staff": false,
    "date_joined": "2024-01-01T00:00:00Z"
  }
}
```

#### Using JWT Token
```bash
curl -X GET http://localhost:8000/api/v1/schedules/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### 4. Protected Endpoints

All schedule endpoints require JWT authentication:
- Include the token in the `Authorization` header
- Format: `Bearer <access_token>`
- Tokens expire after 60 minutes (configurable)
- Use refresh token to get new access tokens

### 5. Token Security Features

- **Token Rotation**: Refresh tokens are rotated on each use
- **Blacklisting**: Old tokens are blacklisted after rotation
- **Expiration**: Access tokens have short lifetimes
- **Custom Claims**: Tokens include user information

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/api/v1/auth/register/` | Register new user | No |
| POST | `/api/v1/auth/login/` | User login | No |
| POST | `/api/v1/auth/token/refresh/` | Refresh JWT token | No |
| GET/PUT/PATCH | `/api/v1/auth/profile/` | User profile | Yes |
| POST | `/api/v1/auth/change-password/` | Change password | Yes |
| POST | `/api/v1/auth/logout/` | User logout | Yes |

### Schedule Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/v1/schedules/` | List user schedules | Yes |
| POST | `/api/v1/schedules/` | Create new schedule | Yes |
| GET | `/api/v1/schedules/{id}/` | Get specific schedule | Yes |
| PUT/PATCH | `/api/v1/schedules/{id}/` | Update schedule | Yes |
| DELETE | `/api/v1/schedules/{id}/` | Delete schedule | Yes |
| GET | `/api/v1/schedules/protected/` | Protected endpoint demo | Yes |
| GET | `/api/v1/schedules/statistics/` | User schedule statistics | Yes |

## Schedule Data Format

The API uses the following JSON structure for schedules:

```json
{
  "name": "My Work Schedule",
  "description": "Weekly work schedule",
  "schedule": {
    "monday": [
      {
        "start": "09:00",
        "stop": "17:00",
        "ids": [1, 2, 3]
      }
    ],
    "tuesday": [
      {
        "start": "10:00",
        "stop": "18:00",
        "ids": [4, 5, 6]
      }
    ],
    "wednesday": [],
    "thursday": [
      {
        "start": "08:00",
        "stop": "16:00",
        "ids": [7, 8, 9, 10]
      }
    ],
    "friday": [
      {
        "start": "09:00",
        "stop": "15:00",
        "ids": [11, 12]
      }
    ],
    "saturday": [],
    "sunday": []
  }
}
```

### Data Validation Rules

- **Time Format**: Use 24-hour format (HH:MM)
- **Start/Stop**: Start time must be before stop time
- **IDs**: Must be a list of positive integers
- **Days**: All seven days must be present (can be empty arrays)
- **Multiple Slots**: Each day can have multiple time slots

## Usage Examples

### Create a Schedule

```bash
curl -X POST http://localhost:8000/api/v1/schedules/ \
  -H "Authorization: Bearer your-jwt-token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Work Schedule",
    "description": "My weekly work schedule",
    "schedule": {
      "monday": [
        {
          "start": "09:00",
          "stop": "17:00",
          "ids": [1, 2, 3]
        }
      ],
      "tuesday": [
        {
          "start": "09:00",
          "stop": "17:00",
          "ids": [1, 2, 3]
        }
      ],
      "wednesday": [],
      "thursday": [
        {
          "start": "10:00",
          "stop": "18:00",
          "ids": [4, 5, 6]
        }
      ],
      "friday": [
        {
          "start": "09:00",
          "stop": "15:00",
          "ids": [1, 2]
        }
      ],
      "saturday": [],
      "sunday": []
    }
  }'
```

### Update a Schedule

```bash
curl -X PUT http://localhost:8000/api/v1/schedules/{schedule-id}/ \
  -H "Authorization: Bearer your-jwt-token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Schedule",
    "description": "Updated description",
    "schedule": {
      "monday": [
        {
          "start": "08:00",
          "stop": "16:00",
          "ids": [1, 2, 3, 4]
        }
      ],
      "tuesday": [],
      "wednesday": [],
      "thursday": [],
      "friday": [],
      "saturday": [],
      "sunday": []
    }
  }'
```

### Get Schedule Statistics

```bash
curl -X GET http://localhost:8000/api/v1/schedules/statistics/ \
  -H "Authorization: Bearer your-jwt-token"
```

## Testing

### Run Unit Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.schedules
python manage.py test apps.authentication

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Test Coverage

The project includes comprehensive test coverage for:
- Model validation and methods
- API endpoints and authentication
- Edge cases and error handling
- Data validation and serialization

## Development

### Code Style

The project follows Python and Django best practices:
- PEP 8 compliance
- Clean architecture with separation of concerns
- Comprehensive documentation
- Type hints where appropriate
- Meaningful variable and function names

### Adding New Features

1. Create models in appropriate app
2. Write serializers for API endpoints
3. Implement views with proper permissions
4. Add URL routing
5. Write comprehensive tests
6. Update documentation

## Security Considerations

- JWT tokens for secure authentication
- Input validation and sanitization
- SQL injection prevention through Django ORM
- CORS configuration for cross-origin requests
- User isolation (users can only access their own data)
- Soft delete for data recovery

## Production Deployment

### Environment Variables

Set the following environment variables for production:

```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:port/database
```

### Database

For production, use PostgreSQL:

```python
# Install psycopg2
pip install psycopg2-binary

# Update settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Static Files

```bash
python manage.py collectstatic
```

## API Rate Limiting

Consider implementing rate limiting for production:

```python
# Install django-ratelimit
pip install django-ratelimit

# Apply to views
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='100/h', method='GET')
def your_view(request):
    pass
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the GitHub repository
- Check the API documentation at `/swagger/`
- Review the test cases for usage examples