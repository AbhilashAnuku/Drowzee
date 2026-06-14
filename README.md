# Drowzee

Interactive preparation and drowsiness tracking platform for students.

Drowzee is a Flask-based final-year project that combines a lightweight learning platform with webcam-based drowsiness monitoring. The goal is to help students stay engaged during preparation sessions by pairing study workflows with fatigue awareness.

## Project Overview

The application provides a web interface for student login, preparation content, and camera-based alertness tracking. It uses OpenCV for video processing and SQLite for local persistence.

## Recruiter Notes

This project demonstrates:

- Flask application structure
- User registration and login flow
- SQLite-backed local persistence
- Webcam integration with OpenCV
- Real-time video streaming through a web interface
- Audio alert behavior for detected drowsiness
- Academic project delivery and documentation

## Features

- Student registration and login
- Session-based access to the learning interface
- Webcam stream inside the web application
- Drowsiness monitoring through camera frames
- Audio feedback when drowsiness is detected
- SQLite schema for local users
- Desktop-like wrapper support through PyFladesk

## Tech Stack

- Python
- Flask
- OpenCV
- SQLite
- Jinja templates
- PyFladesk
- Werkzeug

## Repository Structure

```text
.
├── app.py              # Flask routes and application entry point
├── camera.py           # Camera and drowsiness detection flow
├── base_camera.py      # Streaming camera base class
├── audiopy.py          # Audio alert logic
├── schema.sql          # Database schema
├── requirements.txt    # Python dependencies
├── static/             # Static assets
├── templates/          # HTML templates
├── Usage.md            # Usage notes
└── README.md
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Open the local URL printed by Flask, usually:

```text
http://127.0.0.1:5000
```

## Notes

- Webcam access is required for drowsiness tracking.
- The project is intended as a local academic prototype.
- Local database and cache artifacts should not be treated as production data.

## Future Improvements

- Add automated tests for authentication and camera-independent routes
- Move runtime data into an ignored `instance/` directory
- Add screenshots or a short demo recording
- Split detection logic into a testable service module
