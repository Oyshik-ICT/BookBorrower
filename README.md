# Django Library Management System

## Overview
This is a comprehensive Library Management System built with Django and Django Rest Framework (DRF), featuring user authentication, book borrowing, and fine management.

## Features
- User authentication with JWT
- Book management
- Book borrowing system
- Fine calculation for overdue books
- Role-based permissions (Admin and Member)

## Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)
- Postman (for API testing)

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/Oyshik-ICT/BookBorrower.git

cd BookBorrower
```

### 2. Create a Virtual Environment
```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For MacOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

## Postman API Testing

### Authentication Workflow
1. **Get JWT Token**
   - URL: `POST http://localhost:8000/api/token/`
   - Body (raw JSON):
     ```json
     {
         "username": "your_username",
         "password": "your_password"
     }
     ```
   - This returns an access and refresh token

### Postman Collection Setup
1. Create a new collection in Postman
2. Add a collection-level authorization:
   - Type: Bearer Token
   - Token: Paste the access token from authentication

## API Routes and Permissions

### Authentication Routes
- `POST /api/token/`: Obtain JWT token
- `POST /api/token/refresh/`: Refresh JWT token

### Books Routes
- `GET /books/`: List all books (Members and Admins)
- `POST /books/`: Create a new book (Admin only)
  - Body example:
    ```json
    {
        "title": "Django for Professionals",
        "author": "William S. Vincent",
        "description": "Advanced Django development",
        "price": 500,
        "stock": 10
    }
    ```

### Borrowing Routes
- `GET /borrows/`: List borrows (Admin can see all but Member can see only her/his list)
- `POST /borrows/`: Create a new borrow
  - Body example:
    ```json
    {
        "book_ids": [1, 2, 3]
    }
    ```
- `POST /borrows/{id}/return_books/`: Return borrowed books

### Fine Routes
- `GET /fines/`: List fines (Admins only)
- `POST /fines/{id}/pay/`: Mark a fine as paid (Admins only)

## Borrowing Rules
- Maximum 5 books can be borrowed at a time
- 14-day borrowing period
- 5 taka fine per day for overdue books

## Postman Request Examples

### 1. Obtain JWT Token
- Method: POST
- URL: `http://localhost:8000/api/token/`
- Body (raw JSON):
  ```json
  {
      "username": "admin",
      "password": "adminpassword"
  }
  ```

### 2. Borrow Books
- Method: POST
- URL: `http://localhost:8000/borrows/`
- Headers:
  - Authorization: Bearer `<access_token>`
  - Content-Type: application/json
- Body (raw JSON):
  ```json
  {
      "book_ids": [1, 2]
  }
  ```

### 3. Return Books
- Method: POST
- URL: `http://localhost:8000/borrows/{borrow_id}/return_books/`
- Headers:
  - Authorization: Bearer `<access_token>`

## Troubleshooting
- Ensure all dependencies are installed
- Check that the server is running on `http://localhost:8000`
- Verify user credentials
- Check book availability before borrowing



