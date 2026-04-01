---
# EduNavigator

An AI-powered bachelor's degree recommendation system for Indian students. Students complete a subject-interest quiz, and the system recommends the most suitable degrees based on their aptitude scores. A chat advisor lets students refine recommendations by describing their interests in natural language.

---

## Live Demo
https://edunavigator-sooty.vercel.app/

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19, Vite, React Router, Axios |
| Backend | FastAPI, SQLAlchemy, PostgreSQL |
| Auth | JWT (python-jose), bcrypt |
| AI Chat | Hybrid Recommendation System |

---

## Folder Structure

```
project/
├── backend/
│   ├── .env                          # Environment variables (never commit this)
│   ├── main.py                       # FastAPI app entry point, router registration
│   ├── requirements.txt
│   └── app/
│       ├── core/
│       │   ├── db.py                 # SQLAlchemy engine, session, Base
│       │   ├── deps.py               # JWT auth dependency (get_current_user)
│       │   ├── jwt_handler.py        # create_access_token, verify_token
│       │   └── security.py          # hash_password, verify_password (bcrypt)
│       │
│       ├── models/
│       │   ├── __init__.py           # Exports all models
│       │   ├── user.py               # User table
│       │   ├── profile.py            # UserProfile table (stream, chat_history)
│       │   ├── subject_response.py   # Per-subject interest/performance ratings
│       │   ├── score.py              # Computed aptitude scores per profile
│       │   ├── degree.py             # Degree, DegreeType, Field, Discipline tables
│       │   ├── degree_data.sql       # Seed SQL for degrees
│       │   └── question.py           # (unused, reserved)
│       │
│       ├── routers/
│       │   ├── auth.py               # POST /auth/signup, POST /auth/login
│       │   ├── profile.py            # GET /profile/{profile_id}
│       │   ├── questionnaire.py      # POST /questionnaire/
│       │   ├── recommend.py          # GET /recommend/{profile_id}
│       │   └── chat.py               # POST /chat/, GET /chat/history/{profile_id}
│       │
│       ├── schemas/
│       │   ├── auth.py               # SignupRequest, LoginRequest
│       │   ├── profile.py            # ProfileResponse
│       │   ├── questionnaire.py      # QuestionnaireRequest, SubjectInput
│       │   ├── recommendation.py     # DegreeRecommendation, RecommendationResponse
│       │   └── chat.py               # ChatMessage, ChatResponse
│       │
│       └── services/
│           ├── auth_service.py       # signup(), login() logic
│           ├── questionnaire_service.py  # process_questionnaire(), score calculation
│           ├── scoring_service.py    # recompute_scores() from subject responses
│           ├── recommendation_service.py # generate_recommendations() dot-product scoring
│           └── chat_service.py       # parse_chat_input(), process_chat(), call_claude()
│
└── frontend/
    ├── index.html
    ├── vite.config.js
    ├── package.json
    └── src/
        ├── main.jsx                  # React entry point
        ├── App.jsx                   # Routes definition
        ├── App.css                   # Global styles (dark theme, all component classes)
        ├── index.css
        ├── api.js                    # Axios instance with JWT interceptor
        │
        ├── context/
        │   └── AuthContext.jsx       # Auth state, login(), register(), logout()
        │
        ├── components/
        │   ├── Layout.jsx            # Sidebar + main layout wrapper
        │   ├── ProtectedRoute.jsx    # Redirects unauthenticated users
        │   └── CourseCard.jsx        # Degree recommendation card component
        │
        └── pages/
            ├── Landing.jsx           # Public landing page
            ├── Login.jsx             # Login form
            ├── Register.jsx          # Register form with stream selector
            ├── Quiz.jsx              # Subject interest/performance quiz
            ├── Dashboard.jsx         # Recommendations grid with filters
            ├── Chat.jsx              # AI chat advisor + live recommendations
            └── Admin.jsx             # Admin metrics panel
```

---

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env         # then fill in your values

# Run database migrations
# (tables auto-create on startup via SQLAlchemy)
# Run seed data manually:
psql -U postgres -d edunavigator -f app/models/degree_data.sql

# Add chat_history column if upgrading from older version
psql -U postgres -d edunavigator -c "ALTER TABLE profiles ADD COLUMN IF NOT EXISTS chat_history JSON DEFAULT '[]';"

# Start server
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`, backend at `http://localhost:8000`.

---

## Environment Variables

Create `backend/.env` with the following:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/edunavigator
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Optional — set to "real" to use Claude API, "mock" for keyword parser
LLM_MODE=mock
ANTHROPIC_API_KEY=sk-ant-...
```

> **Never commit `.env` to version control.** Add it to `.gitignore`.

---

## How It Works

### Recommendation Engine

Each degree in the database has five weights: `math_weight`, `science_weight`, `tech_weight`, `commerce_weight`, `arts_weight` (0.0–1.0).

Each student has a `Score` row with corresponding scores built from their quiz responses.

The recommendation score for a degree is a dot product:

```
score = (math_score × math_weight) + (science_score × science_weight)
      + (tech_score × tech_weight) + (commerce_score × commerce_weight)
      + (arts_score × arts_weight)
```

Top degrees by score are returned.

### Chat Advisor

In `mock` mode, the chat service parses keywords from the student's message and applies small boosts to the relevant score categories (e.g. "I love coding" → `tech_score += 2`). Recommendations refresh after each message.

In `real` mode, Claude API is called with the student's profile and score context, and returns a structured JSON reply with suggested score adjustments.

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/auth/signup` | No | Register user + create profile |
| POST | `/auth/login` | No | Login, returns JWT |
| GET | `/profile/{id}` | No | Get profile by ID |
| POST | `/questionnaire/` | Yes | Submit quiz responses |
| GET | `/recommend/{id}` | No | Get top degree recommendations |
| POST | `/chat/` | Yes | Send chat message, get reply + updated recs |
| GET | `/chat/history/{id}` | Yes | Get chat history for profile |
---
