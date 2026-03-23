from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import engine, Base   # ✅ FIXED IMPORT
from app.routers import profile, recommend, chat

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EduNavigator API",
    description="AI-powered bachelor's degree recommendation system",
    version="1.0.0"
)

# CORS — allow frontend (React) to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # update if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(recommend.router, prefix="/recommend", tags=["Recommendation"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])

@app.get("/")
def root():
    return {"message": "Welcome to EduNavigator API"}