from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text
)
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from jinja2 import Template

import os
import requests
import json

# =====================================================
# ENV
# =====================================================

load_dotenv()
print("DATABASE_URL =", os.getenv("DATABASE_URL"))
DATABASE_URL = os.getenv("DATABASE_URL")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# =====================================================
# DATABASE
# =====================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

# =====================================================
# MODELS
# =====================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    total_score = Column(Integer, default=0)


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)

    question = Column(Text)

    option1 = Column(String)
    option2 = Column(String)
    option3 = Column(String)
    option4 = Column(String)

    answer = Column(String)


Base.metadata.create_all(bind=engine)

# =====================================================
# APP
# =====================================================

app = FastAPI()

# =====================================================
# SIMPLE UI
# =====================================================

HTML = """
<html>
<head>
<title>AI Quiz</title>

<style>
body{
background:#111827;
font-family:Arial;
color:white;
text-align:center;
padding:30px;
}

.card{
background:#1f2937;
padding:20px;
width:500px;
margin:auto;
border-radius:10px;
}

button{
padding:10px;
margin:5px;
width:80%;
cursor:pointer;
}

input{
padding:10px;
width:80%;
margin:10px;
}
</style>

</head>

<body>

<div class="card">

{{content}}

</div>

</body>

</html>
"""

# =====================================================
# GLOBAL SESSION
# =====================================================

# GLOBAL SESSION

CURRENT_USER = None

CURRENT_QUESTIONS = []
CURRENT_INDEX = 0

# =====================================================
# OPENROUTER
# =====================================================

import requests
import json

def generate_ai_questions(topic, count=5):

    prompt = f"""
Generate {count} multiple choice questions on {topic}.

Return ONLY JSON array.

[
  {{
    "question":"...",
    "options":["A","B","C","D"],
    "answer":"..."
  }}
]
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "google/gemini-2.5-flash",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    result = response.json()

    content = result["choices"][0]["message"]["content"]

    content = content.replace("```json", "")
    content = content.replace("```", "")

    return json.loads(content)
# =====================================================
# HOME
# =====================================================

@app.get("/", response_class=HTMLResponse)
def home():

    content = """
    <h1>AI Quiz</h1>

    <form action="/register" method="post">
        <input name="username" placeholder="Username">
        <button>Start</button>
    </form>

    <br>

    <a href="/leaderboard">
        <button>Leaderboard</button>
    </a>
    """

    return Template(HTML).render(content=content)

# =====================================================
# REGISTER USER
# =====================================================

@app.post("/register")
def register(username: str = Form(...)):

    global CURRENT_USER

    db = SessionLocal()

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:

        user = User(
            username=username,
            total_score=0
        )

        db.add(user)
        db.commit()

    CURRENT_USER = username

    return RedirectResponse(
        "/topic",
        status_code=303
    )

# =====================================================
# TOPIC PAGE
# =====================================================

@app.get("/topic", response_class=HTMLResponse)
def topic_page():

    content = """
    <h2>Choose Topic</h2>

    <form action="/generate" method="post">

        <input
            name="topic"
            placeholder="Java, Movies, Finance..."
        >

        <button>
            Generate Question
        </button>

    </form>
    """

    return Template(HTML).render(content=content)

# =====================================================
# GENERATE QUESTION
# =====================================================

@app.post("/generate", response_class=HTMLResponse)
def generate(topic: str = Form(...)):

    global CURRENT_QUESTIONS
    global CURRENT_INDEX

    questions = generate_ai_questions(topic, 5)

    CURRENT_QUESTIONS = questions
    CURRENT_INDEX = 0

    db = SessionLocal()

    for q in questions:

        db.add(
            Question(
                question=q["question"],
                option1=q["options"][0],
                option2=q["options"][1],
                option3=q["options"][2],
                option4=q["options"][3],
                answer=q["answer"]
            )
        )

    db.commit()

    q = CURRENT_QUESTIONS[CURRENT_INDEX]

    content = f"""
    <h2>{q['question']}</h2>

    <form action="/answer" method="post">

        <button name="answer" value="{q['options'][0]}">
            {q['options'][0]}
        </button>

        <button name="answer" value="{q['options'][1]}">
            {q['options'][1]}
        </button>

        <button name="answer" value="{q['options'][2]}">
            {q['options'][2]}
        </button>

        <button name="answer" value="{q['options'][3]}">
            {q['options'][3]}
        </button>

    </form>
    """

    return Template(HTML).render(content=content)
    

# =====================================================
# ANSWER
# =====================================================
@app.post("/answer", response_class=HTMLResponse)
def answer(answer: str = Form(...)):

    global CURRENT_INDEX
    global CURRENT_QUESTIONS
    global CURRENT_USER

    db = SessionLocal()

    user = (
        db.query(User)
        .filter(User.username == CURRENT_USER)
        .first()
    )

    if CURRENT_INDEX >= len(CURRENT_QUESTIONS):
        return HTMLResponse("<h1>Quiz Finished</h1>")

    q = CURRENT_QUESTIONS[CURRENT_INDEX]

    # Case-insensitive comparison
    correct = (
        answer.strip().lower()
        ==
        q["answer"].strip().lower()
    )

    # Update score
    if correct:
        user.total_score += 10
        db.commit()

    feedback = "✅ Correct! +10 XP" if correct else "❌ Wrong!"

    CURRENT_INDEX += 1

    # Quiz Finished
    if CURRENT_INDEX >= len(CURRENT_QUESTIONS):

        content = f"""
        <h1>🎉 Quiz Finished</h1>

        <h2>{feedback}</h2>

        <h3>Final Score: {user.total_score}</h3>

        <a href="/leaderboard">
            <button>View Leaderboard</button>
        </a>

        <br><br>

        <a href="/topic">
            <button>Play Again</button>
        </a>
        """

        return HTMLResponse(
            content=Template(HTML).render(content=content)
        )

    next_q = CURRENT_QUESTIONS[CURRENT_INDEX]

    content = f"""
    <h3>{feedback}</h3>

    <h3>Current Score: {user.total_score}</h3>

    <h2>{next_q['question']}</h2>

    <form action="/answer" method="post">

        <button name="answer" value="{next_q['options'][0]}">
            {next_q['options'][0]}
        </button>

        <button name="answer" value="{next_q['options'][1]}">
            {next_q['options'][1]}
        </button>

        <button name="answer" value="{next_q['options'][2]}">
            {next_q['options'][2]}
        </button>

        <button name="answer" value="{next_q['options'][3]}">
            {next_q['options'][3]}
        </button>

    </form>
    """

    return HTMLResponse(
        content=Template(HTML).render(content=content)
    )

# =====================================================
# LEADERBOARD
# =====================================================

@app.get("/leaderboard", response_class=HTMLResponse)
def leaderboard():

    db = SessionLocal()

    users = (
        db.query(User)
        .order_by(User.total_score.desc())
        .limit(10)
        .all()
    )

    rows = ""

    for index, user in enumerate(users, start=1):

        rows += f"""
        <p>
        {index}. {user.username}
        - {user.total_score}
        XP
        </p>
        """

    content = f"""
    <h1>Leaderboard</h1>

    {rows}

    <a href="/">
        <button>
            Home
        </button>
    </a>
    """

    return Template(HTML).render(content=content)

# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )