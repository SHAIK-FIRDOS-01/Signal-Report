# SignalReport 🛰️

**SignalReport** is a high-performance, AI-driven news intelligence platform designed to cut through the noise of the modern information landscape. Using cutting-edge LLMs and real-time news ingestion, it provides deep analysis, credibility scoring, and interactive contextual intelligence.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.13%2B-blue.svg)
![React](https://img.shields.io/badge/react-18.x-61DAFB.svg)

---

## ✨ Key Features

- **Real-Time Intelligence**: Automated news ingestion via GNews API with support for global headlines.
- **AI Deep Analysis**: Multi-paragraph intelligence reports powered by **Groq (Llama 3.3 70B)** for lightning-fast inference.
- **Interactive Digest**:
  - **Contextual Q&A**: Ask follow-up questions about any news article.
  - **Smart Glossary**: Highlight terms to get general definitions blended with news-specific context.
- **Credibility Scoring**: Automated AI assessment of source reliability and content integrity.
- **Premium UI/UX**: Responsive, glassmorphic dashboard built for visual excellence and mobile-first accessibility.
- **Semantic Search**: Vector-ready architecture for future RAG (Retrieval-Augmented Generation) enhancements.

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 5.0 (Python 3.13)
- **AI Engine**: Groq SDK (Llama 3.3 / 8B)
- **Database**: MySQL (for primary storage)
- **Processing**: Async task handling for news ingestion and AI enhancement.

### Frontend
- **Framework**: React + Vite
- **Styling**: Vanilla CSS (Custom Design System)
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
DB_HOST=127.0.0.1
DB_PORT=3306

# APIs
GNEWS_API_KEY=your_gnews_key
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key

# Django
SECRET_KEY=your_secret_key
DEBUG=True
```

---

## 🛡️ Security & Privacy
- **Environment Safety**: All API keys and database credentials are excluded from version control via `.gitignore`.
- **Authentication**: JWT-based authentication for secure access to intelligence reports.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

---

*Developed with ❤️ by the SignalReport Team.*
