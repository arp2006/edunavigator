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
