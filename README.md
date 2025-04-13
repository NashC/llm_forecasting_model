# LLM Financial Forecasting Platform

An AI-driven web application that enables financial professionals to create, refine, and share financial models through a conversational interface powered by Large Language Models.

## Features

- **AI-Powered Conversation Interface**: Generate financial models by describing them in natural language
- **Dynamic Model Generation**: Automatically create Python code for financial forecasts
- **Interactive Web Dashboard**: Visualize forecasts with charts and tables, adjust parameters in real-time
- **Multi-Format Export**: Export to Python scripts, Google Sheets, Excel, or CSV
- **Version Control**: Save different iterations of your models and track changes
- **Data Import**: Connect to various data sources for historical data
- **Secure Collaboration**: Share models with team members securely

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (relational data), MongoDB (model storage)
- **Authentication**: JWT-based auth with refresh tokens
- **LLM Integration**: OpenAI API (GPT-4)
- **Data Processing**: Pandas, NumPy, Matplotlib

### Frontend  
- **Framework**: React with Material-UI
- **State Management**: React Context API
- **Data Visualization**: Chart.js, Recharts
- **Form Handling**: Formik with Yup validation

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Deployment**: Cloud-ready (AWS, Azure, GCP)
- **CI/CD**: GitHub Actions ready

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 16+ (for local frontend development)
- Python 3.9+ (for local backend development)
- OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/llm-financial-forecasting.git
   cd llm-financial-forecasting
   ```

2. Create backend environment variables:
   ```bash
   cp backend/.env.example backend/.env
   ```
   
3. Edit the `.env` file to add your OpenAI API key and database credentials.

4. Start the application using Docker Compose:
   ```bash
   docker-compose up -d
   ```

5. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## Project Structure

```
├── backend             # FastAPI backend
│   ├── app             # Application code
│   │   ├── api         # API endpoints
│   │   ├── auth        # Authentication
│   │   ├── core        # Core settings
│   │   ├── db          # Database models
│   │   ├── models      # Pydantic schemas
│   │   └── services    # Business logic
│   ├── migrations      # Database migrations
│   └── tests           # Backend tests
├── frontend            # React frontend
│   ├── public          # Static files
│   └── src             # React code
│       ├── components  # UI components
│       ├── contexts    # React contexts
│       ├── hooks       # Custom hooks
│       ├── pages       # Page components
│       ├── services    # API services
│       └── utils       # Utility functions
├── data                # Data directory
├── scripts             # Utility scripts
└── docs                # Documentation
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- OpenAI for their powerful LLM APIs
- The FastAPI and React communities for their excellent frameworks
- All contributors to the open-source libraries used in this project 