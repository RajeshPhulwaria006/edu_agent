# EduAgent --- AI Configuration & Architecture Guide

> Contributor-oriented technical guide for understanding the AI layer,
> backend flow, data flow, and project architecture.

Repository: https://github.com/RajeshPhulwaria006/edu_agent

------------------------------------------------------------------------

## 1. What is EduAgent?

EduAgent is a full-stack student academic analytics system.

Its core responsibility is to take structured student academic data,
store it, calculate performance indicators, predict academic risk with a
machine-learning model, and generate natural-language academic analysis
and recommendations.

At a high level:

``` text
Student / Faculty
       │
       ▼
React Frontend
       │
       │ HTTP / REST
       ▼
FastAPI Backend
       │
       ├──────────────► SQLite / SQLAlchemy
       │
       ├──────────────► ML Risk Predictor
       │
       └──────────────► AI Academic Agent
                              │
                              ▼
                         Groq LLM
                              │
                              ▼
                    Analysis / Recommendation
```

The important architectural idea is that **the LLM is not the source of
the student's raw academic truth**.

The backend first retrieves and aggregates structured data. That
structured result is then passed to the AI agent as context. This keeps
the AI layer focused on interpretation rather than database access or
uncontrolled data collection.

------------------------------------------------------------------------

# 2. Repository Structure

Current repository structure:

``` text
edu_agent/
│
├── .env.example
├── .gitignore
├── README.md
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── seed.py
│   ├── requirements.txt
│   │
│   ├── routes/
│   │   ├── students.py
│   │   ├── performance.py
│   │   └── ai_agent.py
│   │
│   └── ml/
│       ├── agents_config.py
│       └── predictor.py
│
└── frontend/
    ├── index.html
    ├── package.json
    │
    └── src/
        ├── App.jsx
        ├── main.jsx
        ├── index.css
        │
        ├── components/
        │   ├── Navbar.jsx
        │   ├── PerformanceCard.jsx
        │   └── Sidebar.jsx
        │
        ├── pages/
        │   ├── Dashboard.jsx
        │   ├── Students.jsx
        │   ├── StudentProfile.jsx
        │   └── AIAdvisor.jsx
        │
        └── services/
            └── api.js
```

Think of the repository as four logical layers:

``` text
Frontend
   ↓
API / Application Layer
   ↓
Data + ML Layer
   ↓
AI Interpretation Layer
```

------------------------------------------------------------------------

# 3. Responsibility of Each Layer

## Frontend

The React frontend is responsible for:

-   Displaying students
-   Displaying performance
-   Showing dashboards
-   Showing student profiles
-   Calling backend APIs
-   Displaying AI-generated analysis

Important locations:

``` text
frontend/src/pages/
frontend/src/components/
frontend/src/services/api.js
```

The frontend should **not** contain business-critical academic
calculations or API credentials.

It is primarily a presentation and interaction layer.

------------------------------------------------------------------------

## FastAPI Backend

The backend is the central application layer.

`backend/main.py` creates the FastAPI application and registers:

``` text
students router
performance router
AI router
```

The backend also configures CORS and initializes the database tables.

Conceptually:

``` text
HTTP Request
     │
     ▼
FastAPI Router
     │
     ▼
Application Logic
     │
     ├── Database
     ├── ML
     └── AI Agent
```

------------------------------------------------------------------------

## Database Layer

The database layer contains:

``` text
database.py
models.py
schemas.py
seed.py
```

The current project uses SQLite with SQLAlchemy.

The database represents persistent application state.

Typical conceptual relationship:

``` text
Student
  │
  └──< Performance
```

A student can have multiple performance records.

The AI layer does not directly query the database. The route layer
retrieves the required records and prepares an input object for the AI
agent.

------------------------------------------------------------------------

# 4. ML Layer vs AI Agent Layer

One of the most important architectural distinctions in this project is:

``` text
ML Prediction
      ≠
LLM Analysis
```

They solve different problems.

## Machine Learning

`backend/ml/predictor.py`

The current model is a Random Forest classifier.

Input features:

``` text
attendance
internal marks
assignment marks
practical marks
quiz marks
previous CGPA
```

Output:

``` text
risk = HIGH / LOW
high_risk_probability = percentage
```

The current predictor is a demonstration model trained on a small
synthetic dataset.

Therefore, contributors should not treat its probability as a
production-calibrated academic risk score.

------------------------------------------------------------------------

## LLM Agent

`backend/ml/agents_config.py`

The LLM is responsible for:

-   Interpreting structured performance
-   Summarizing strengths
-   Identifying weak areas
-   Producing actionable recommendations

It does **not** train the Random Forest model.

It does **not** replace the database.

It does **not** calculate the student's academic metrics.

The architecture is therefore:

``` text
Structured Academic Data
          │
          ├──────────────► ML Model
          │                    │
          │                    ▼
          │               Risk Prediction
          │
          └──────────────► LLM Agent
                               │
                               ▼
                      Human-readable insight
```

------------------------------------------------------------------------

# 5. AI Configuration

The main AI configuration is located at:

``` text
backend/ml/agents_config.py
```

The file defines:

``` python
class Agent:
```

The class encapsulates:

1.  Agent identity
2.  Agent description
3.  LLM configuration
4.  Analysis prompt
5.  Recommendation prompt
6.  LangChain execution pipeline

This is useful because routes do not need to know how the LLM is
configured internally.

Instead:

``` python
ai_agent.analyze(...)
```

or:

``` python
ai_agent.recommend(...)
```

acts as the abstraction boundary.

------------------------------------------------------------------------

# 6. LLM Initialization

The agent loads the API key from environment variables:

``` python
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
```

The model is initialized using:

``` python
ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)
```

### Why temperature = 0?

The application is an analytical system rather than a creative chatbot.

A low temperature encourages more deterministic responses.

The desired behavior is:

``` text
same input
   ↓
similar analytical output
```

rather than highly varied creative responses.

The API key must remain in `.env` and must never be committed to Git.

------------------------------------------------------------------------

# 7. LangChain Pipeline

Both AI operations use the same conceptual pipeline:

``` text
PromptTemplate
      │
      ▼
ChatGroq
      │
      ▼
StrOutputParser
      │
      ▼
String response
```

In code:

``` python
chain = prompt_template | self.model | parser
```

This is LangChain's Runnable composition model.

Each component has one responsibility:

### PromptTemplate

Builds the final prompt from:

``` text
input
name
description
```

### ChatGroq

Sends the generated prompt to the configured Groq-hosted LLM.

### StrOutputParser

Converts the model response into a plain string.

This keeps the AI execution pipeline simple and easy to replace later.

------------------------------------------------------------------------

# 8. Agent Identity and Description

The constructor receives:

``` python
Agent(name, description)
```

This separates the generic agent implementation from the specific role.

For example:

``` python
Agent(
    name="Student performance analyser",
    description="..."
)
```

The prompt then receives these values dynamically:

``` text
You are {name}.
{description}
```

This means the same `Agent` abstraction could later support different
educational roles without duplicating the entire LLM integration.

For example, future agents could conceptually be:

``` text
Performance Analyst
Academic Advisor
Attendance Advisor
Faculty Assistant
Study Planner
```

The current project only needs the academic analysis/advisory behavior.

------------------------------------------------------------------------

# 9. Analyze Flow

The `analyze()` method is designed to produce a compact academic
analysis.

Its expected conceptual output contains:

``` text
1. Overall performance
2. Strongest areas
3. Weakest areas
4. Areas needing improvement
5. One actionable recommendation
```

The important constraint is:

``` text
Use only the supplied student data.
Do not fabricate information.
Do not make unsupported assumptions.
```

This is important for educational analytics because the LLM should
interpret the available evidence rather than inventing student
characteristics.

------------------------------------------------------------------------

# 10. Recommendation Flow

The `recommend()` method has a slightly different responsibility.

It focuses on:

``` text
Weak areas
      ↓
Specific improvement actions
      ↓
Study priorities
      ↓
Strength reinforcement
      ↓
Practical next step
```

The intended output is 4--5 concise recommendations.

The prompt also explicitly asks the model to avoid unsupported
recommendations.

This makes `analyze()` and `recommend()` conceptually different:

``` text
analyze()
    ↓
"What does the data say?"

recommend()
    ↓
"What should the student work on based on that data?"
```

------------------------------------------------------------------------

# 11. End-to-End AI Request Flow

The most important flow for a new contributor to understand is:

``` text
Frontend
   │
   │ GET /ai/advisor/{student_id}
   ▼
routes/ai_agent.py
   │
   ├── Find Student
   │
   ├── Find Performance Records
   │
   ├── Calculate averages
   │
   ├── Identify weak subjects
   │
   ├── Build structured input
   │
   ▼
Agent.analyze()
   │
   ├── PromptTemplate
   │
   ├── ChatGroq
   │
   └── StrOutputParser
   │
   ▼
LLM response
   │
   ▼
FastAPI JSON response
   │
   ▼
React AI Advisor page
```

------------------------------------------------------------------------

# 12. How Student Data Becomes AI Input

The AI route retrieves all performance records belonging to the
requested student.

It calculates aggregate values such as:

``` text
Average attendance
Average internal marks
Average assignment marks
Average practical marks
Average quiz marks
Previous CGPA
```

It also calculates subject-level averages:

``` text
subject_avg =
(
    internal_marks
    + assignment_marks
    + practical_marks
    + quiz_marks
) / 4
```

Subjects below the configured threshold are collected as weak subjects.

The final AI input is conceptually:

``` python
{
    "student_name": "...",
    "attendance": ...,
    "internal_marks": ...,
    "practical_marks": ...,
    "assignment_marks": ...,
    "quiz": ...,
    "previous_cgpa": ...,
    "weak_subjects": [...],
    "subjects_avg": {...}
}
```

This object is the bridge between the structured backend and the LLM.

------------------------------------------------------------------------

# 13. Why the Route Prepares the Data

A new contributor might wonder:

> Why not let the LLM calculate everything from raw database records?

Because that would mix responsibilities.

The better architectural boundary is:

``` text
Database
   ↓
Backend
   ↓
Validated / aggregated academic context
   ↓
LLM
```

The backend owns deterministic calculations.

The LLM owns language-based interpretation.

For example:

``` text
Average attendance = 72.4%
```

should be calculated by Python.

But:

``` text
Attendance appears to be an area that may require improvement.
```

can be generated by the LLM.

This separation improves reproducibility, testing, and maintainability.

------------------------------------------------------------------------

# 14. API Boundary

The AI feature is exposed through:

``` text
GET /ai/advisor/{student_id}
```

The endpoint:

1.  Receives a student ID.
2.  Retrieves the student.
3.  Retrieves performance records.
4.  Validates that enough data exists.
5.  Aggregates performance.
6.  Calls the AI agent.
7.  Returns the generated analysis.

Successful response conceptually looks like:

``` json
{
    "student_id": 1,
    "student_name": "Student Name",
    "response": "Generated academic analysis..."
}
```

If the student does not exist:

``` json
{
    "response": "Student not found."
}
```

If performance records do not exist:

``` json
{
    "response": "Not enough performance data."
}
```

------------------------------------------------------------------------

# 15. Full System Architecture

The current architecture can be understood as five major components:

``` text
                    ┌─────────────────────┐
                    │   React Frontend    │
                    │                     │
                    │ Dashboard            │
                    │ Students             │
                    │ Profile              │
                    │ AI Advisor           │
                    └──────────┬──────────┘
                               │
                         REST / HTTP
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    │                     │
                    │ main.py             │
                    │ routes/             │
                    └───────┬─────┬───────┘
                            │     │
                 ┌──────────┘     └──────────┐
                 ▼                           ▼
        ┌─────────────────┐          ┌─────────────────┐
        │ Database Layer  │          │   ML / AI Layer │
        │                 │          │                 │
        │ SQLAlchemy      │          │ Random Forest   │
        │ SQLite          │          │ AI Agent        │
        └─────────────────┘          └────────┬────────┘
                                              │
                                              ▼
                                      ┌─────────────────┐
                                      │ Groq LLM API    │
                                      │ GPT-OSS-120B    │
                                      └─────────────────┘
```

------------------------------------------------------------------------

# 16. Separation of Responsibilities

A contributor should preserve these boundaries.

  Component            Responsibility
  -------------------- -------------------------------------
  React                UI and user interaction
  `api.js`             Frontend API communication
  FastAPI routes       Request handling and orchestration
  SQLAlchemy models    Database representation
  Database             Persistent student/performance data
  `predictor.py`       ML risk prediction
  `agents_config.py`   LLM configuration and prompting
  Groq                 LLM inference
  Pydantic schemas     API input/output validation

Avoid putting all logic into one file.

For example:

``` text
Bad:
route → database + ML training + prompt + UI logic

Better:
route
 ├── database
 ├── ML service
 └── AI agent
```

------------------------------------------------------------------------

# 17. Current ML Architecture

The current predictor uses:

``` text
Input features
     │
     ▼
RandomForestClassifier
     │
     ├── Prediction
     │
     └── Probability
```

The model uses:

``` text
attendance
internal
assignment
practical
quiz
previous_cgpa
```

and returns:

``` python
{
    "risk": "HIGH" or "LOW",
    "high_risk_probability": ...
}
```

### Important contributor note

The current training data is demonstration data embedded directly inside
`predictor.py`.

It should therefore be treated as a prototype implementation.

For institutional use, the training pipeline should eventually become:

``` text
Historical Student CSV
        │
        ▼
Data Validation
        │
        ▼
Feature Engineering
        │
        ▼
Train / Validation Split
        │
        ▼
Model Training
        │
        ▼
Evaluation
        │
        ▼
Model Artifact
        │
        ▼
Inference Service
```

------------------------------------------------------------------------

# 18. Current AI Architecture

The AI architecture is currently stateless.

There is no conversational memory.

Each request is effectively:

``` text
Student data
     +
Agent identity
     +
Agent description
     +
Prompt instructions
     ↓
LLM
     ↓
Response
```

The LLM does not retain previous student conversations through this
class.

This is desirable for the current academic analysis use case because
each analysis should be grounded in the current structured student data.

------------------------------------------------------------------------

# 19. Prompt Design Principles

The current prompts follow several useful principles.

## Grounding

The prompt explicitly provides student data.

``` text
Student Performance:
{input}
```

The model should reason from that context.

## Role definition

The model receives an explicit role:

``` text
academic performance advisor
```

or:

``` text
academic performance analyst
```

## Output constraints

The prompts constrain the response format.

This reduces unnecessary verbosity and makes the response easier for the
frontend to display.

## Anti-hallucination instruction

The prompt explicitly states:

``` text
Do not make assumptions.
Do not fabricate details.
Use only the given data.
```

These instructions are especially important when the system is used for
student-related decisions.

------------------------------------------------------------------------

# 20. Contributor Workflow

When modifying the AI layer, follow this flow:

``` text
1. Understand the data structure
        ↓
2. Check how the route builds AI input
        ↓
3. Modify prompt / agent logic
        ↓
4. Test with deterministic sample data
        ↓
5. Check API response
        ↓
6. Check frontend rendering
        ↓
7. Verify no API key is exposed
        ↓
8. Commit changes
```

Do not modify prompts blindly.

First inspect the object being passed to:

``` python
ai_agent.analyze(...)
```

or:

``` python
ai_agent.recommend(...)
```

The prompt can only reason about information that is actually present in
that object.

------------------------------------------------------------------------

# 21. Where to Make Common Changes

## Change LLM model

Modify:

``` text
backend/ml/agents_config.py
```

Specifically the `ChatGroq(...)` configuration.

------------------------------------------------------------------------

## Change analysis behavior

Modify:

``` text
Agent.analyze()
```

------------------------------------------------------------------------

## Change recommendation behavior

Modify:

``` text
Agent.recommend()
```

------------------------------------------------------------------------

## Change student data sent to the LLM

Modify:

``` text
backend/routes/ai_agent.py
```

The object passed to `ai_agent.analyze()` controls the available
context.

------------------------------------------------------------------------

## Change ML risk logic

Modify:

``` text
backend/ml/predictor.py
```

------------------------------------------------------------------------

## Change API endpoint behavior

Modify:

``` text
backend/routes/
```

------------------------------------------------------------------------

## Change frontend AI display

Modify:

``` text
frontend/src/pages/AIAdvisor.jsx
```

------------------------------------------------------------------------

# 22. Environment Configuration

The AI integration requires:

``` text
GROQ_API_KEY=your_api_key
```

Recommended local structure:

``` text
backend/
├── .env
├── requirements.txt
└── ...
```

`.env` should never be committed.

`.env.example` should contain only the variable name or a placeholder.

Example:

``` env
GROQ_API_KEY=your_groq_api_key
```

------------------------------------------------------------------------

# 23. Request Lifecycle Example

Suppose a faculty member opens:

``` text
Student Profile → AI Advisor
```

The frontend requests:

``` text
GET /ai/advisor/42
```

The backend:

``` text
1. Finds Student #42
2. Loads performance records
3. Calculates averages
4. Calculates subject averages
5. Identifies weak subjects
6. Builds the AI context dictionary
7. Sends it to Agent.analyze()
```

The agent:

``` text
PromptTemplate
      ↓
GPT-OSS-120B through Groq
      ↓
StrOutputParser
```

Then the backend returns:

``` text
JSON
   ↓
React
   ↓
AI Advisor UI
```

This is the complete AI request lifecycle.

------------------------------------------------------------------------

# 24. Important Architectural Principle

The project should be treated as:

``` text
Data → Deterministic Processing → Prediction / Interpretation → Presentation
```

not:

``` text
Data → LLM → Everything
```

The distinction matters.

### Deterministic responsibilities

Use Python/database/ML for:

-   Data retrieval
-   Aggregation
-   Feature calculation
-   Threshold calculations
-   Risk model inference
-   Validation

### Generative responsibilities

Use the LLM for:

-   Natural-language analysis
-   Explanation
-   Personalized wording
-   Recommendation generation

This separation makes the system easier to debug.

------------------------------------------------------------------------

# 25. Current Limitations

The repository README identifies several prototype-level limitations:

-   The ML model uses a small synthetic dataset.
-   SQLite is currently used for local development.
-   There is no authentication or role-based access control.
-   The advisory layer requires production-grade validation and
    evaluation.
-   Production deployment would require stronger privacy and security
    controls.
-   The model should eventually be trained and validated on appropriate
    historical academic data.

These limitations are important context for contributors.

The current architecture demonstrates the integration pattern, but it
should not be treated as an institution-ready predictive system without
further validation.

------------------------------------------------------------------------

# 26. Recommended Future Architecture

A more production-oriented version could evolve toward:

``` text
                 React Frontend
                       │
                       ▼
                API Gateway / FastAPI
                       │
          ┌────────────┼─────────────┐
          ▼            ▼             ▼
       Student       ML Service    AI Service
       Service          │             │
          │             ▼             ▼
          │         Model Store     LLM API
          │
          ▼
      PostgreSQL
          │
          ▼
   Historical Data / ETL
```

The ML pipeline could become:

``` text
CSV / Institutional Data
        ↓
Validation
        ↓
Cleaning
        ↓
Feature Engineering
        ↓
Training
        ↓
Evaluation
        ↓
Model Registry
        ↓
Inference
```

The AI service could eventually add:

``` text
Structured context
       ↓
Prompt builder
       ↓
LLM
       ↓
Structured output validation
       ↓
Response
```

------------------------------------------------------------------------

# 27. Production Improvements for the AI Layer

Before production deployment, consider adding:

## Structured output

Instead of returning arbitrary text, define a schema such as:

``` json
{
    "overall": "...",
    "strengths": [],
    "weaknesses": [],
    "improvement_areas": [],
    "recommendations": []
}
```

This makes frontend rendering more reliable.

## Prompt versioning

Keep prompts versioned so changes can be tracked.

Example:

``` text
analysis_prompt_v1
analysis_prompt_v2
```

## Evaluation

Create a small evaluation dataset containing:

``` text
student data
expected analytical behavior
undesired behavior
```

Then compare model outputs when changing prompts or models.

## Logging

Log:

``` text
request ID
student ID
prompt version
model name
latency
success/failure
```

Avoid logging sensitive student information unnecessarily.

## Timeout and retry handling

External LLM calls can fail.

The service should eventually handle:

``` text
timeout
rate limit
API failure
invalid response
```

without crashing the entire API.

------------------------------------------------------------------------

# 28. Security Principles

Never:

``` text
commit GROQ_API_KEY
```

Never expose the API key to React.

The correct flow is:

``` text
React
  ↓
FastAPI
  ↓
Groq
```

not:

``` text
React
  ↓
Groq API directly
```

The server should own the secret.

For production academic data, also consider:

-   Authentication
-   Authorization
-   Encryption in transit
-   Database access controls
-   Audit logging
-   Input validation
-   Data minimization
-   Appropriate retention policies

------------------------------------------------------------------------

# 29. Mental Model for New Contributors

If you remember only one diagram, remember this:

``` text
                  USER
                   │
                   ▼
             React Frontend
                   │
                   ▼
              FastAPI API
                   │
          ┌────────┼─────────┐
          │        │         │
          ▼        ▼         ▼
       Database    ML       AI Agent
          │        │         │
          │        │         ▼
          │        │       Groq
          │        │         │
          │        │         ▼
          │        │    Text Analysis
          │        │
          │        ▼
          │     Risk Score
          │
          ▼
    Academic Records
```

The backend is the orchestrator.

The database stores facts.

The ML model predicts.

The LLM explains and recommends.

The frontend presents everything to the user.

------------------------------------------------------------------------

# 30. Quick File Map

  File                                      Understand it as
  ----------------------------------------- ----------------------------------
  `backend/main.py`                         Application entry point
  `backend/database.py`                     Database connection/session
  `backend/models.py`                       SQLAlchemy database models
  `backend/schemas.py`                      API validation schemas
  `backend/seed.py`                         Demo data initialization
  `backend/routes/students.py`              Student API
  `backend/routes/performance.py`           Performance API
  `backend/routes/ai_agent.py`              AI orchestration/API
  `backend/ml/predictor.py`                 Random Forest risk prediction
  `backend/ml/agents_config.py`             LLM agent + prompts
  `frontend/src/services/api.js`            Frontend → backend communication
  `frontend/src/pages/AIAdvisor.jsx`        AI result UI
  `frontend/src/pages/Dashboard.jsx`        Analytics dashboard
  `frontend/src/pages/StudentProfile.jsx`   Student-level view
  `frontend/src/pages/Students.jsx`         Student listing

------------------------------------------------------------------------

# 31. First Files to Read as a New Contributor

Read the project in this order:

``` text
1. README.md
       ↓
2. backend/main.py
       ↓
3. backend/models.py
       ↓
4. backend/routes/students.py
       ↓
5. backend/routes/performance.py
       ↓
6. backend/routes/ai_agent.py
       ↓
7. backend/ml/predictor.py
       ↓
8. backend/ml/agents_config.py
       ↓
9. frontend/src/services/api.js
       ↓
10. frontend/src/pages/AIAdvisor.jsx
```

This order follows the system's dependency flow rather than simply
reading files alphabetically.

------------------------------------------------------------------------

# 32. Final Architectural Summary

EduAgent is currently a **full-stack academic analytics prototype** with
three important intelligence paths:

``` text
                     Student Data
                          │
             ┌────────────┼────────────┐
             │            │            │
             ▼            ▼            ▼
         Analytics       ML           LLM
             │            │            │
             │            ▼            ▼
             │       Risk Prediction  Explanation
             │                         +
             │                    Recommendations
             └────────────┬────────────┘
                          ▼
                    React Dashboard
```

The central design principle is separation of concerns:

``` text
Database → stores
Backend  → orchestrates
ML       → predicts
LLM      → interprets
React    → presents
```

For a new contributor, the most important AI boundary is:

``` text
backend/routes/ai_agent.py
          │
          │ structured student context
          ▼
backend/ml/agents_config.py
          │
          │ prompt
          ▼
      Groq LLM
          │
          ▼
      text result
          │
          ▼
       FastAPI
          │
          ▼
        React
```

Understanding this flow is enough to safely navigate, debug, and extend
the current AI architecture.
