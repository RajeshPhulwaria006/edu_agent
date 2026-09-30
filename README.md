# EduAgent

**AI-Powered Student Performance Prediction & Academic Advisory System**

EduAgent is a full-stack academic analytics system that combines **React.js, FastAPI, SQLite, and Scikit-learn** to manage student records, analyze academic performance, predict academic risk, and provide personalized rule-based academic recommendations.

> **Note:** The current ML model is a demonstration model trained on a small synthetic dataset. The academic advisor is rule-based.

---

## ✨ Features

* 👨‍🎓 Student management
* 📊 Academic performance tracking
* 📈 Performance analysis dashboard
* 🤖 Random Forest–based risk prediction
* 💡 Rule-based academic recommendations
* 📉 Performance visualization with Recharts
* 🔌 REST API with FastAPI
* 🗄️ SQLite database with SQLAlchemy
* 📖 Interactive Swagger API documentation

---

## 🏗️ Architecture

```text
React.js Frontend
       │
       │ REST API
       ▼
FastAPI Backend
   ┌───┼───────────────┐
   ▼   ▼               ▼
SQLite  ML Predictor   Advisor
        │              │
        ▼              ▼
   Random Forest   Rule-Based Logic
```

---

## 📁 Project Structure

```text
eduagent/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── seed.py
│   ├── requirements.txt
│   ├── routes/
│   │   ├── students.py
│   │   ├── performance.py
│   │   └── ai_agent.py
│   └── ml/
│       └── predictor.py
│
└── frontend/
    ├── package.json
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── index.css
        ├── services/
        │   └── api.js
        ├── components/
        │   └── ...
        └── pages/
            ├── Dashboard.jsx
            ├── Students.jsx
            ├── StudentProfile.jsx
            └── AIAdvisor.jsx
```

---

## 🛠️ Tech Stack

| Layer      | Technology          |
| ---------- | ------------------- |
| Frontend   | React.js, Vite      |
| UI         | CSS, Recharts       |
| Backend    | FastAPI             |
| Database   | SQLite, SQLAlchemy  |
| Validation | Pydantic            |
| ML         | Scikit-learn, NumPy |
| API Client | Axios               |

---

## 🚀 Installation

### Backend

```bash
cd eduagent/backend

python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Initialize demo data:

```bash
python seed.py
```

Initialize GROQ api key in backend/.env

```text
GROQ_API_KEY="your-api-key"
```
Start the API:

```bash
cd backend
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend

```bash
cd eduagent/frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## 🔌 Core API Endpoints

| Method   | Endpoint                     | Purpose             |
| -------- | ---------------------------- | ------------------- |
| `POST`   | `/students/`                 | Create student      |
| `GET`    | `/students/`                 | List students       |
| `GET`    | `/students/{id}`             | Get student         |
| `DELETE` | `/students/{id}`             | Delete student      |
| `POST`   | `/performance/`              | Add performance     |
| `GET`    | `/performance/{id}`          | Get performance     |
| `GET`    | `/performance/{id}/analysis` | Analyze performance |
| `GET`    | `/ai/advisor/{id}`           | Get academic advice |

---

## 🤖 ML & Advisory System

The prediction model uses:

* Attendance
* Internal marks
* Assignment marks
* Practical marks
* Quiz marks
* Previous CGPA

A **Random Forest Classifier** produces a `HIGH` or `LOW` academic-risk prediction with a high-risk probability.

The academic advisor analyzes performance using predefined academic rules and generates recommendations such as improving attendance, completing assignments, and increasing practical preparation.

---

## ⚠️ Current Limitations

The current version is intended as a working demonstration.

* ML model uses a small synthetic dataset.
* No authentication or role-based access.
* SQLite is used for local development.
* Academic advisor is rule-based.
* Production deployment requires stronger privacy, security, validation, and model evaluation.

For a real institutional deployment, the model should be trained and validated using appropriate historical academic data.

---

## 🔮 Future Improvements

* PostgreSQL + Alembic migrations
* JWT authentication and RBAC
* Production ML training pipeline
* Model monitoring and versioning
* Advanced recommendation engine
* Student/faculty dashboards
* Docker deployment
* CI/CD
* Privacy and audit controls

---

## 📄 License

This project is intended for educational and development purposes.
