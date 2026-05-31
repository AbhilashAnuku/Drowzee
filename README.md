# Drowzee
# Final Year Project  
## Interactive Preparation and Drowsiness Tracking Platform for Students(LMS)

### Overview  
This project provides an **Interactive Learning Management System (LMS)** integrated with a **drowsiness detection mechanism**. It is designed to enhance student engagement, track fatigue during study sessions, and ensure effective preparation for academic goals. The platform incorporates both **video streaming** and **user authentication** for personalized usage.

---

## Features  
1. **Interactive LMS Platform**  
   - User authentication: Register, login, and session management.
   - Course management: Students access courses, resources, and learning material.
   - Progress tracking through quizzes, assignments, and study logs.

2. **Drowsiness Detection System**  
   - Video feed from webcam to monitor student’s alertness.
   - Uses real-time drowsiness detection algorithms to alert users if drowsiness is detected.
   - **Audio alerts** for specific conditions (e.g., 100% drowsiness score triggers sound notification).

3. **SQLite Database Integration**  
   - Stores user credentials securely with **hashed passwords** using `werkzeug.security`.
   - Tracks session details and activity logs.

4. **Flask-based Web App with Pyfladesk Integration**  
   - **Web GUI** initialized using Pyfladesk to provide a desktop application-like experience.
   - Video streaming and drowsiness tracking through the browser.

---

## Project Structure  
```bash
📂 Final Year Project
│
├── 📂 static
│ ├── story.mp3 
│
├── 📂 templates
│ ├── index.html 
│ ├── login.html
│ ├── register.html 
│
├── camera.py # Camera class for video streaming and detection
├── audiopy.py # Audio playback logic for alerts
├── main.py # Flask application with all routes
├── users.db # SQLite database
├── requirements.txt
└── README.md 
