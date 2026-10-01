# EduAgent — Project Summary

EduAgent is a full-stack **student academic analytics platform** designed to analyze student performance, identify academic risk patterns, and provide personalized academic insights.

The system uses **React** for the frontend and **FastAPI** for the backend, with **SQLite/SQLAlchemy** for student and performance data. Its intelligence layer combines **Machine Learning** for academic risk prediction with a **Groq-hosted LLM agent** for natural-language analysis and recommendations.

### Core Flow

```text
Student Academic Data
        ↓
   FastAPI Backend
        ↓
 ┌──────┴─────────┐
 ↓                ↓
ML Predictor    AI Agent
 ↓                ↓
Risk Analysis   LLM Analysis
 └──────┬─────────┘
        ↓
   React Dashboard
```

### Main Capabilities

* Student and academic performance management
* Performance aggregation and analysis
* ML-based academic risk prediction
* AI-generated student performance analysis
* Personalized improvement recommendations
* Student dashboard and profile views
* REST API architecture for frontend/backend communication

### Technology Stack

**Frontend:** React, Vite, JavaScript
**Backend:** Python, FastAPI
**Database:** SQLite, SQLAlchemy
**Machine Learning:** Scikit-learn, Random Forest
**AI/LLM:** LangChain, Groq, GPT-OSS-120B
**API Communication:** REST / HTTP

### Architectural Principle

EduAgent separates deterministic computation from generative AI:

```text
Database → stores academic facts
Backend  → processes and orchestrates
ML       → predicts academic risk
LLM      → explains and recommends
Frontend → presents insights
```

This makes the project easier to extend toward a production-grade academic analytics system while keeping the ML and LLM responsibilities clearly separated.
