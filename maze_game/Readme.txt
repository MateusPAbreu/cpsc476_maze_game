# 🧩 The Math Maze Game  
A Django-based maze game where kids solve math problems to unlock doors and race to the exit.

---

## 📌 Overview
The Math Maze Game is an interactive browser-based game built with **Python** and **Django**.  
Players navigate a randomly generated maze, encounter locked doors, solve math problems, and compete against an AI opponent whose difficulty changes based on the selected level.

This README explains how to install dependencies, create a virtual environment, run the project, and understand the project folder structure.

---

# 📁 Project Structure

```
maze_game/
│
├── maze_app/                    # Main Django application
│   ├── migrations/              # Database migration files
│   │
│   ├── static/
│   │   ├── audio/               # Background music + tutorial audio
│   │   │   ├── mazemusic.mp3
│   │   │   └── music.mp3
│   │   │
│   │   ├── scripts/             # JS scripts folder
│   │   │
│   │   ├── styles/              # Images + stylesheets
│   │   │   ├── FirstMaze.png
│   │   │   ├── Maze_tutorial.mp4
│   │   │   ├── menu.png
│   │   │   ├── options.png
│   │   │   └── styles.css
│   │
│   ├── templates/               # HTML templates for all pages
│   │   ├── ai.html
│   │   ├── index.html
│   │   ├── maze.html
│   │   ├── menu.html
│   │   ├── options.html
│   │   ├── play.html
│   │   ├── select.html
│   │   └── tutorial.html
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
│
├── maze_game/                   # Django project configuration folder
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── db.sqlite3                   # SQLite database
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
└── CPSC 476 Final Presentation.pptx
```

---

# 🛠️ Requirements  
- Python **3.10+**  
- pip  
- Virtual environment support (`venv`)  
- Django 

Everything needed is in:

```
requirements.txt
```

---

# 🚀 How to Install & Run the Game

Follow these steps:

---

## 1️⃣ Create a Virtual Environment

### **Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

### **macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should now see:

```
(venv)
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Apply Migrations

```bash
python manage.py migrate
```

---

## 4️⃣ Run the Server

```bash
python manage.py runserver
```

Open the game in your browser:

👉 **http://127.0.0.1:8000/**

---

# 🎮 Gameplay Summary

- Choose a difficulty level (1–5)  
- Roll dice to move through the maze  
- Solve math questions to open doors  
- AI opponent tries to reach the goal  
- AI door logic changes based on difficulty  
- Includes narration and background music  

---


### This submission includes:
- Full Django project directory  
- `requirements.txt`  
- `README.md`  
- Presentation slides  

---

# 🔧 Useful Developer Commands

### Create a superuser:
```bash
python manage.py createsuperuser
```

### Collect static files (for deployment):
```bash
python manage.py collectstatic
```

# To access admin page
👉 **http://127.0.0.1:8000/admin**
Username: gdspark
Password: Gdspark123.


