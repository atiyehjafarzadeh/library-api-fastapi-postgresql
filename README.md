# Library API (FastAPI + PostgreSQL)

A library management REST API built with FastAPI, SQLAlchemy, and PostgreSQL. It lets users create, retrieve, update, and delete books, with all data persisted in a PostgreSQL database.

## Features

- Retrieve all books
- Add a new book
- Retrieve a book by ID
- Partially update a book using PATCH
- Delete a book by ID
- Persistent storage with PostgreSQL
- Request validation with Pydantic
- Proper error handling (404 for missing books, 422 for invalid data)
- Automatically generated interactive API documentation (Swagger UI and ReDoc)

## Technologies

- Python
- FastAPI
- Pydantic
- SQLAlchemy (ORM)
- PostgreSQL
- Psycopg2
- python-dotenv
- Uvicorn

## Project Structure

```text
library-api-fastapi-postgresql/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.10 or newer
- PostgreSQL installed and running
- Git

## Installation

### 1. Clone the Repository

Replace `YOUR_USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR_USERNAME/library-api-fastapi-postgresql.git
cd library-api-fastapi-postgresql
```

### 2. Create a Virtual Environment (recommended)

```bash
python -m venv venv
```

Activate it:

```bash
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL

Create a database for the project. For example, using `psql`:

```sql
CREATE DATABASE library_db;
```

### 5. Configure Environment Variables

Copy the example file and fill in your own database credentials:

```bash
cp .env.example .env          # Linux / macOS
copy .env.example .env        # Windows
```

Then edit `.env`:

```text
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/library_db
```

| Part | Description |
|---|---|
| `USER` | Your PostgreSQL username (default is often `postgres`) |
| `PASSWORD` | Your PostgreSQL password |
| `localhost:5432` | Database host and port |
| `library_db` | The database name you created |

**Important:** Never commit your real `.env` file. It is listed in `.gitignore`. If your password contains special characters (such as `@` or `#`), URL-encode them.

### 6. Run the Application

```bash
uvicorn main:app --reload
```

The server will start at:

http://127.0.0.1:8000

The `books` table is created automatically on startup if it does not exist.

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

You can use Swagger UI to test all endpoints directly in your browser.

## API Endpoints

| Method | Endpoint | Description | Success Status |
|---|---|---|---|
| GET | `/books` | Retrieve all books | 200 |
| POST | `/books` | Add a new book | 201 |
| GET | `/books/{id}` | Retrieve a book by ID | 200 |
| PATCH | `/books/{id}` | Update a book | 200 |
| DELETE | `/books/{id}` | Delete a book | 204 |

## Example Requests

### 1. Retrieve All Books

```http
GET /books
```

Returns a list of all books, ordered by ID.

```bash
curl http://127.0.0.1:8000/books
```

### 2. Add a New Book

```http
POST /books
```

Request body:

```json
{
  "title": "Python Crash Course",
  "author": "Eric Matthes",
  "year": 2019,
  "available": true
}
```

```bash
curl -X POST http://127.0.0.1:8000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Python Crash Course", "author": "Eric Matthes", "year": 2019, "available": true}'
```

Response (`201 Created`):

```json
{
  "title": "Python Crash Course",
  "author": "Eric Matthes",
  "year": 2019,
  "available": true,
  "id": 1
}
```

### 3. Retrieve a Book by ID

```http
GET /books/1
```

Returns the details of the book with ID `1`. If the book does not exist, the API returns `404 Not Found`.

### 4. Update a Book

```http
PATCH /books/1
```

Request body:

```json
{
  "available": false
}
```

```bash
curl -X PATCH http://127.0.0.1:8000/books/1 \
  -H "Content-Type: application/json" \
  -d '{"available": false}'
```

Only the fields provided in the request are updated. Other fields remain unchanged. Explicitly provided `null` values are rejected with `422 Unprocessable Entity`.

### 5. Delete a Book

```http
DELETE /books/1
```

```bash
curl -X DELETE http://127.0.0.1:8000/books/1
```

Returns `204 No Content` on success, or `404 Not Found` if the book does not exist.

## Error Responses

| Status | Meaning |
|---|---|
| 404 Not Found | The requested book does not exist |
| 422 Unprocessable Entity | Invalid request data (for example, an empty title, a negative year, or a `null` value in PATCH) |

Example error body:

```json
{
  "detail": "Book not found"
}
```

## Data Storage

Book data is stored in a PostgreSQL database and persists across application restarts. The connection is configured through the `DATABASE_URL` environment variable, and the database is accessed using the SQLAlchemy ORM.

### Books Table

| Column | Type | Notes |
|---|---|---|
| id | Integer | Primary key, auto-incremented |
| title | String(255) | Required |
| author | String(255) | Required |
| year | Integer | Optional |
| available | Boolean | Required, defaults to `true` |

## Troubleshooting

- **`DATABASE_URL is not set in .env`**: Make sure you created a `.env` file (copied from `.env.example`) in the same directory as `main.py`.
- **`connection refused` or `could not connect to server`**: Make sure PostgreSQL is running and the host and port in `DATABASE_URL` are correct.
- **`password authentication failed`**: Check the username and password in `DATABASE_URL`.
- **`database "library_db" does not exist`**: Create the database first (see step 4).

## License

This project was developed for educational purposes.