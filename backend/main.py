from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes.students import router as student_router
from routes.performance import router as performance_router
from routes.ai_agent import router as ai_router

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="EduAgent API",
    description="AI Student Performance & Academic Advisor",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(student_router)
app.include_router(performance_router)
app.include_router(ai_router)

@app.get("/")
def home():
    return {"message": "EduAgent API is running successfully"}
