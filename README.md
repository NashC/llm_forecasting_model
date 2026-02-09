# LLM Financial Forecasting Platform

A web application that lets financial professionals create and refine forecasting models through natural language conversation. Describe what you want to forecast, and the system generates executable Python code, visualizations, and exportable models using GPT-4.

## How it works

1. **User describes a forecast** in plain English (e.g., "Build a 12-month revenue forecast using seasonal decomposition")
2. **Backend sends the conversation to GPT-4**, which generates Python forecasting code using Prophet, statsmodels, or custom models
3. **Generated code executes server-side**, producing time series data and chart-ready output
4. **Frontend renders interactive dashboards** with Chart.js and Recharts, allowing parameter adjustments in real time
5. **Models are versioned and exportable** to Python scripts, Excel, or CSV

## Technical Architecture

```
Frontend (React + Material-UI)      Backend (FastAPI)
┌──────────────────────────┐       ┌──────────────────────────────┐
│ Chat interface           │──────▶│ /api/chat/message            │
│ Dashboard + charts       │       │ /api/chat/generate-forecast  │
│ Model management         │       │ /api/financial_models (CRUD) │
│ Auth (JWT)               │       │ /api/data_sources            │
└──────────────────────────┘       └──────────┬───────────────────┘
                                              │
                            ┌─────────────────┼─────────────────┐
                            │                 │                 │
                       PostgreSQL          MongoDB         OpenAI API
                       (users, auth)    (model storage)    (GPT-4)
```

**Why two databases**: User accounts, sessions, and auth tokens are relational — PostgreSQL handles these with ACID guarantees and Alembic migrations. Generated forecasting models vary in structure (different parameters, assumptions, time horizons), so they're stored as documents in MongoDB where schema flexibility avoids constant migrations as model types evolve.

**Backend**: FastAPI with async endpoints, JWT authentication (access + refresh tokens), and Alembic migrations.

**Frontend**: React 18 with Material-UI, Chart.js and Recharts for visualization, Formik/Yup for forms, Context API for state management.

**Forecasting**: GPT-4 generates Python code using Prophet (time series), statsmodels (ARIMA, seasonal decomposition), pandas, and NumPy. Results are serialized and sent to the frontend for rendering.

## Quick Start

```bash
# Clone and configure
git clone https://github.com/NashC/llm_forecasting_model.git
cd llm_forecasting_model
cp backend/.env.example backend/.env
# Add your OpenAI API key and database credentials to backend/.env

# Start everything
docker-compose up -d

# Access the app
# Frontend: http://localhost:3000
# API docs: http://localhost:8000/docs
```

### Local development

```bash
# Backend
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend && npm install && npm start
```

## What I'd improve next

- Add test coverage (test directory scaffolded but empty)
- Stream LLM responses instead of waiting for full generation
- Support additional LLM providers beyond OpenAI
- Add data source connectors (CSV upload, database connections, API integrations)
