# SignalReport 🛰️

**SignalReport** is a high-performance, AI-driven news intelligence platform designed to cut through the noise of the modern information landscape. Using cutting-edge LLMs and real-time news ingestion, it provides deep analysis, credibility scoring, and interactive contextual intelligence.

![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.13%2B-blue.svg)
![React](https://img.shields.io/badge/react-18.x-61DAFB.svg)

---

## ✨ Key Features

- **Real-Time Intelligence**: Automated news ingestion via GNews API with support for global headlines and specific technical categories.
- **AI Deep Analysis**: Multi-paragraph intelligence reports powered by **Groq (Llama 3.3 70B)** for lightning-fast inference and deep semantic understanding.
- **Interactive Digest**:
  - **Contextual Q&A**: Ask follow-up questions about any news article using RAG-ready context.
  - **Smart Glossary**: Highlight complex terms to get general definitions blended with real-time news context.
- **Credibility Scoring**: Automated AI assessment of source reliability, sentiment, and content integrity.
- **Premium UI/UX**: Responsive, glassmorphic dashboard built for visual excellence, micro-animations, and mobile-first accessibility.
- **Semantic Search**: Vector-ready architecture for advanced knowledge retrieval and intelligence mapping.

---

## 🛠️ Tech Stack

### Backend (The Core)
- **Framework**: Django 5.0 (Python 3.13)
- **AI Engine**: Groq SDK (Llama 3.3 / 8B)
- **Database**: MySQL 8.0 (Enterprise-ready storage)
- **NLP**: Custom processing for entity extraction and sentiment analysis.

### Frontend (The Interface)
- **Framework**: React + Vite
- **Styling**: Vanilla CSS (Custom Design System with Glassmorphism)
- **Icons**: Lucide-React
- **State Management**: React Hooks & Context API

---

## 📂 Project Structure

```text
ai_news_analyst/
├── backend/                # Django API & AI Services
│   ├── apps/               # Business logic (Accounts, Knowledge Base)
│   ├── core/               # Django Settings & Routing
│   ├── services/           # AI, Scrapers, and NLP Processing
│   ├── venv/               # Virtual Environment
│   └── .env                # Secrets (API Keys, DB Credentials)
├── frontend/               # React Dashboard
│   ├── src/                # Source code (Components, Hooks)
│   └── public/             # Static Assets
└── .gitignore              # Security and Build rules
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- Node.js & npm
- MySQL Server

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Activate venv:
# Windows: .\venv\Scripts\activate
# Linux/macOS: source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Environment Variables
Create a `.env` file in the `backend/` directory with the following:
```env
# Database
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port

# APIs
GNEWS_API_KEY=Keep your APIs here
GROQ_API_KEY=Keep your APIs here
GEMINI_API_KEY=Keep your APIs here

# Django
SECRET_KEY=your_django_secret_key_here
DEBUG=True
ALLOWED_HOSTS=your_domain.com,localhost
```

---

## 🛡️ Security & Privacy
- **Environment Safety**: All API keys and database credentials are excluded from version control via `.gitignore`.
- **Zero-Trust Ready**: JWT-based authentication for secure access to intelligence reports.
- **Data Integrity**: Automated validation of incoming news sources and content.

## 📄 License
This project is licensed under the **Apache License 2.0** - see the LICENSE file for details.

---

*Developed with ❤️ by the SignalReport Team.*
