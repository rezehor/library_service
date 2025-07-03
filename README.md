# 📚 Library Service API

## Description
Library Service is a web-based Django application that helps manage book borrowings and payments in a modern library system.

It allows users to:
- Browse available books
- Borrow and return books
- View their borrowing history
- Handle payments via Stripe
- Notify admins via Telegram on borrowing events


## Project Features:
- **Book Management:** View books, authors. Admins can add/update/delete books
- **Borrowing System:** Authenticated users can borrow/return books. View borrow history.
- **Payment Integration:** Stripe session generation.
- **Telegram Notifications:** Send alerts on borrow events
- **Admin Panel:** Admins can add, edit, and delete all data through a built-in interface.
- **Authentication:** Users log in and get a JWT token to access protected features.
- **Permissions:**
  - Guests can view books, but not borrow
  - Registered users can view everything and borrow books
  - Admins have full access to all actions


## Installation and Setup

To get started with the Library Service API, follow these steps:

### Step 1: Clone the Repository

```bash
git clone https://github.com/rezehor/library_service.git
```

### Step 2: Prepare the Environment
Make sure you have the following installed:

- Python 3.10 or higher

- PostgreSQL database

- Docker (optional)

Create and activate a virtual environment:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Environment Variables
Create a .env file and provide the required values:
```bash
POSTGRES_PASSWORD=POSTGRES_PASSWORD
POSTGRES_USER=POSTGRES_USER
POSTGRES_DB=POSTGRES_DB
POSTGRES_HOST=db
POSTGRES_PORT=5432
PGDATA=/var/lib/postgresql/data

SECRET_KEY=SECRET_KEY

TELEGRAM_BOT_TOKEN=TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID=TELEGRAM_CHAT_ID

STRIPE_SECRET_KEY=STRIPE_SECRET_KEY
STRIPE_PUBLISHABLE_KEY=STRIPE_PUBLISHABLE_KEY
```

### Step 5: Database Setup
Run the following commands to apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Run the Server
```bash
python manage.py runserver
```

### Optional: Run with Docker
Make sure Docker and Docker Compose are installed and running:
```bash
docker-compose build
docker-compose up
```

### Getting Access:
- **create a user:** /api/user/register
- **get access token:** /api/user/token
