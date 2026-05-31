# AI Quiz Generator

An AI-powered quiz generation web application that dynamically creates multiple-choice questions using Google's Gemini 2.5 Flash model through OpenRouter API.

Users can enter a topic, generate quizzes instantly, answer questions, earn points, and compete on a leaderboard.

---

# Features

* User Registration
* AI-Generated Quiz Questions
* Topic-Based Quiz Creation
* Real-Time Scoring System
* Leaderboard Ranking
* PostgreSQL Database Storage
* FastAPI Backend
* OpenRouter Integration
* Gemini 2.5 Flash Model
* AWS EC2 Deployment

---

# Tech Stack

## Backend

* FastAPI
* Python 3
* Uvicorn

## Database

* PostgreSQL
* SQLAlchemy ORM

## AI Services

* OpenRouter API
* Google Gemini 2.5 Flash

## Cloud Deployment

* AWS EC2

## Additional Libraries

* python-dotenv
* requests
* jinja2

---

# Project Structure

```bash
.
│
├── main.py
├── .env
├── requirements.txt
├── README.md
│
└── PostgreSQL Database
```

---

# ⚙️ System Architecture

User
↓
FastAPI Web Application
↓
OpenRouter API
↓
Gemini 2.5 Flash
↓
Generated Quiz Questions
↓
PostgreSQL Database
↓
Leaderboard & User Scores

---

# Database Design

## Users Table

| Field       | Type    |
| ----------- | ------- |
| id          | Integer |
| username    | String  |
| total_score | Integer |

Purpose:
Stores registered users and cumulative quiz scores.

---

## Questions Table

| Field    | Type    |
| -------- | ------- |
| id       | Integer |
| question | Text    |
| option1  | String  |
| option2  | String  |
| option3  | String  |
| option4  | String  |
| answer   | String  |

Purpose:
Stores AI-generated quiz questions and answers.

---

# Environment Variables

Create a .env file:

```env
DATABASE_URL=postgresql://username:password@hostname:5432/database_name

OPENROUTER_API_KEY=your_openrouter_api_key
```

---

# Installation

Clone Repository

```bash
git clone https://github.com/yourusername/ai-quiz-generator-fastapi.git

cd ai-quiz-generator-fastapi
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary requests python-dotenv jinja2 python-multipart
```

---

#  Run Application

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Open Browser:

```text
http://localhost:8000
```

---

# Application Workflow

1. User enters username.
2. User selects quiz topic.
3. FastAPI sends prompt to OpenRouter.
4. Gemini 2.5 Flash generates MCQs.
5. Questions are stored in PostgreSQL.
6. User answers questions.
7. System evaluates responses.
8. Score is updated.
9. Leaderboard displays top users.

---

# AWS Deployment

The application is deployed on AWS EC2.

Deployment Steps:

* Launch Ubuntu EC2 Instance
* Configure Security Groups
* Clone GitHub Repository
* Create Virtual Environment
* Install Dependencies
* Configure Environment Variables
* Start FastAPI Server
* Access via Public IP Address

Example:

http://EC2_PUBLIC_IP:8000

---

# API Endpoints

| Endpoint     | Method | Description      |
| ------------ | ------ | ---------------- |
| /            | GET    | Home Page        |
| /register    | POST   | Register User    |
| /topic       | GET    | Topic Selection  |
| /generate    | POST   | Generate AI Quiz |
| /answer      | POST   | Submit Answer    |
| /leaderboard | GET    | View Leaderboard |

---

# Sample Topics

* Artificial Intelligence
* Machine Learning
* Python
* Java
* Finance
* Cloud Computing
* Data Structures
* Movies
* Sports
* Cyber Security

---

# Learning Outcomes

This project demonstrates:

* FastAPI Development
* REST API Concepts
* SQLAlchemy ORM
* PostgreSQL Integration
* Environment Variable Management
* Prompt Engineering
* OpenRouter API Integration
* Gemini AI Integration
* AWS EC2 Deployment
* Cloud Hosting

---

# Future Enhancements

* User Authentication
* Session Management
* JWT Tokens
* PostgreSQL Connection Pooling
* Docker Deployment
* HTTPS Support
* Nginx Reverse Proxy
* Quiz Categories
* Difficulty Levels
* Timed Quizzes
* Admin Dashboard

---

# AWS Link
http://3.110.182.133:8000/



---

# 📄 License

This project is developed for educational and academic purposes.
