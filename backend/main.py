from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import engine, Base   # ✅ FIXED IMPORT
from app.routers import auth, profile, recommend, chat, questionnaire
import os
from dotenv import load_dotenv

load_dotenv()

FRONTEND = os.getenv("FRONTEND")

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EduNavigator API",
    description="AI-powered bachelor's degree recommendation system",
    version="1.0.0"
)

# CORS — allow frontend (React) to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND],  # update if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(recommend.router, prefix="/recommend", tags=["Recommendation"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(questionnaire.router, prefix="/questionnaire", tags=["Questionnaire"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    return {"message": "Welcome to EduNavigator API"}