# EduNavigator — Backend

AI-powered degree recommendation system backend built with FastAPI + PostgreSQL.

## Project Structure

```
edunavigator/
├── main.py                  # FastAPI app entry point
├── requirements.txt
├── .env.example
└── app/
    ├── database.py          # PostgreSQL connection & session
    ├── models.py            # SQLAlchemy ORM models
    ├── schemas.py           # Pydantic request/response schemas
    ├── engine.py            # Recommendation engine (hybrid logic)
    └── routers/
        ├── profile.py       # POST/GET/PATCH /profile
        ├── recommend.py     # GET /recommend/{id}
        └── chat.py          # POST /chat
```

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up PostgreSQL
```bash
# Create the database
psql -U postgres -c "CREATE DATABASE edunavigator;"
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env with your DB credentials
```

### 4. Run the server
```bash
uvicorn main:app --reload
```

### 5. Explore the API
Open http://localhost:8000/docs for the interactive Swagger UI.

## API Endpoints

| Method | Endpoint             | Description                          |
|--------|----------------------|--------------------------------------|
| POST   | /profile/            | Create a student profile             |
| GET    | /profile/{id}        | Get a student profile                |
| PATCH  | /profile/{id}        | Update a student profile             |
| GET    | /recommend/{id}      | Get degree recommendations           |
| POST   | /chat/               | Chat-based refinement of results     |

## Recommendation Engine

The engine uses a **hybrid approach**:

- **Content-based (70%)**: Matches user aptitude scores and interests against degree requirements and tags.
- **Collaborative filtering simulation (10%)**: Uses work style to infer field affinity based on patterns from similar users.
- **Explicit preferences (20%)**: Boosts degrees in fields the user explicitly selected.

### Scoring weights
| Component       | Weight |
|-----------------|--------|
| Aptitude match  | 40%    |
| Interest overlap| 30%    |
| Field preference| 20%    |
| Work style fit  | 10%    |
