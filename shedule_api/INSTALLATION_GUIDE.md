# Django Schedule API - Installation Guide

This guide will walk you through setting up the Django Schedule API project from scratch on your local machine.

## Prerequisites

Before starting, make sure you have the following installed:

- **Python 3.8+** (recommended: Python 3.11)
- **pip** (Python package installer)
- **Git** (for cloning the repository)
- **virtualenv** or **venv** (for creating virtual environments)

### Check Prerequisites

```bash
# Check Python version
python --version
# or
python3 --version

# Check pip
pip --version
# or
pip3 --version

# Check Git
git --version
```

## Step 1: Clone or Create Project Directory

### Option A: If you have a Git repository
```bash
git clone <your-repository-url>
cd schedule_api
```

### Option B: Create new project directory
```bash
mkdir schedule_api
cd schedule_api
```

## Step 2: Create Virtual Environment

### Using venv (recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Using virtualenv (alternative)
```bash
# Install virtualenv if not installed
pip install virtualenv

# Create virtual environment
virtualenv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

**Note:** Your terminal prompt should show `(venv)` when the virtual environment is activated.

## Step 3: Create Project Structure

If you're starting from scratch, create the following directory structure:

```bash
# Create main project directories
mkdir -p schedule_api
mkdir -p apps/core
mkdir -p apps/schedules
mkdir -p apps/authentication

# Create __init__.py files
touch schedule_api/__init__.py
touch apps/__init__.py
touch apps/core/__init__.py
touch apps/schedules/__init__.py
touch apps/authentication/__init__.py
```

## Step 4: Create Requirements File

Create `requirements.txt` with the following content:

```txt
Django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
drf-yasg==1.21.7
python-decouple==3.8
psycopg2-binary==2.9.9
django-cors-headers==4.3.1
coverage==7.3.2
```

## Step 5: Install Python Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

**If you encounter issues:**
- On Windows, you might need to install Microsoft Visual C++ Build Tools
- On macOS, you might need to install Xcode command line tools: `xcode-select --install`
- On Linux, you might need to install development packages: `sudo apt-get install python3-dev libpq-dev`

## Step 6: Create Django Project Structure

### Create Django project (if starting fresh)
```bash
# Create Django project
django-admin startproject schedule_api .

# Navigate to project directory
cd schedule_api

# Create Django apps
python manage.py startapp core ../apps/core
python manage.py startapp schedules ../apps/schedules
python manage.py startapp authentication ../apps/authentication
```

## Step 7: Environment Configuration

Create a `.env` file in the project root:

```bash
# Create .env file
touch .env
```

Add the following content to `.env`:

```bash
# Django settings
SECRET_KEY=django-insecure-development-key-change-in-production-!@#$%^&*()
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database settings (SQLite for development)
# DATABASE_URL=sqlite:///db.sqlite3

# JWT settings (optional - defaults are provided)
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=10080

# CORS settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000
```

## Step 8: Copy Project Files

Copy all the provided code files to their respective locations:

```
schedule_api/
├── schedule_api/
│   ├── __init__.py
│   ├── settings.py          # Copy provided settings
│   ├── urls.py              # Copy provided main URLs
│   ├── wsgi.py             # Django auto-generated
│   └── asgi.py             # Django auto-generated
├── apps/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py        # Copy provided core models
│   │   ├── managers.py      # Copy provided managers
│   │   └── admin.py         # Copy provided admin config
│   ├── schedules/
│   │   ├── __init__.py
│   │   ├── models.py        # Copy provided schedule models
│   │   ├── serializers.py   # Copy provided serializers
│   │   ├── views.py         # Copy provided views
│   │   ├── urls.py          # Copy provided URLs
│   │   ├── admin.py         # Copy provided admin config
│   │   └── tests.py         # Copy provided tests
│   └── authentication/
│       ├── __init__.py
│       ├── serializers.py   # Copy provided auth serializers
│       ├── views.py         # Copy provided auth views
│       ├── urls.py          # Copy provided auth URLs
│       ├── admin.py         # Copy provided admin config
│       └── tests.py         # Copy provided auth tests
├── requirements.txt
├── manage.py               # Django auto-generated
├── .env                   # Environment variables
├── .env.example          # Copy provided example
└── .gitignore            # Copy provided gitignore
```

## Step 9: Database Setup

```bash
# Create and apply migrations
python manage.py makemigrations core
python manage.py makemigrations schedules
python manage.py makemigrations authentication
python manage.py migrate

# Create superuser (optional but recommended)
python manage.py createsuperuser
```

Follow the prompts to create a superuser account.

## Step 10: Verify Installation

### Start the development server
```bash
python manage.py runserver
```

You should see output like:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 20, 2024 - 10:00:00
Django version 4.2.7, using settings 'schedule_api.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Test the installation

1. **Open your browser** and go to: `http://localhost:8000/`
2. **You should see the Swagger UI** with the API documentation
3. **Admin interface**: `http://localhost:8000/admin/` (login with superuser credentials)

### Test API endpoints

```bash
# Test API health (in a new terminal)
curl http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com", 
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'
```

## Step 11: Run Tests

```bash
# Run all tests
python manage.py test

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Step 12: Test with Sample Script

Run the provided sample API requests:

```bash
python sample_api_requests.py
```

This will test all API endpoints automatically.

## Troubleshooting

### Common Issues and Solutions

#### 1. **ModuleNotFoundError: No module named 'apps'**
- Make sure you have `__init__.py` files in all directories
- Verify your `PYTHONPATH` includes the project root

#### 2. **Import errors**
- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

#### 3. **Database errors**
- Delete `db.sqlite3` and migration files (except `__init__.py`)
- Run migrations again: `python manage.py migrate`

#### 4. **Port already in use**
- Use a different port: `python manage.py runserver 8001`
- Or kill the process using port 8000

#### 5. **Permission errors on Windows**
- Run terminal as Administrator
- Or use different virtual environment location

#### 6. **psycopg2 installation issues**
- For development, you can comment out `psycopg2-binary` from requirements.txt
- SQLite will be used by default

### Verify Everything Works

✅ **Server starts without errors**
✅ **Swagger UI loads at** `http://localhost:8000/`
✅ **Admin interface accessible at** `http://localhost:8000/admin/`
✅ **Tests pass:** `python manage.py test`
✅ **Sample script runs successfully:** `python sample_api_requests.py`

## Next Steps

1. **Explore the API** using Swagger UI at `http://localhost:8000/`
2. **Register a user** via the API or admin interface
3. **Create schedules** using the POST `/api/v1/schedules/` endpoint
4. **Test JWT authentication** by including Bearer tokens in requests
5. **Review the code structure** to understand the implementation

## Development Workflow

```bash
# Daily development workflow
source venv/bin/activate  # Activate virtual environment
python manage.py runserver  # Start development server

# When making model changes
python manage.py makemigrations
python manage.py migrate

# Run tests frequently
python manage.py test

# Before committing
python manage.py test
coverage run --source='.' manage.py test
coverage report
```

## Production Considerations

For production deployment:

1. **Environment variables**: Use proper values in `.env`
2. **Database**: Switch to PostgreSQL
3. **Static files**: Configure static file serving
4. **Security**: Update `SECRET_KEY`, set `DEBUG=False`
5. **HTTPS**: Use SSL certificates
6. **CORS**: Configure proper allowed origins

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Ensure virtual environment is activated
4. Review Django and DRF documentation
5. Check the project's README.md for additional information

## Summary

You now have a fully functional Django Schedule API with:
- ✅ JWT Authentication
- ✅ CRUD operations for schedules
- ✅ Swagger documentation
- ✅ Comprehensive tests
- ✅ Clean code architecture

The API is ready for development and testing!