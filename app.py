#!/usr/bin/env python
import os
import sys
import datetime
import threading
import sqlite3
from flask import Flask, render_template, Response, request, redirect, session
from pyfladesk import init_gui
from camera import Camera, resource_path
from audiopy import start_player
from werkzeug.security import generate_password_hash, check_password_hash

perfect = resource_path(os.path.join('static', 'perfect.mp3'))
icon = resource_path(os.path.join('static', 'appicon.png'))

if getattr(sys, 'frozen', False):
    template_folder = resource_path('templates')
    static_folder = resource_path('static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

webcam = Camera()

# SQLite database connection
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize SQLite database schema
def initialize_database():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

initialize_database()

# Define video streaming generator function
def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        try:
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            if user and check_password_hash(user['password'], password):
                session['username'] = username
                return redirect('/')  # Redirect to video streaming page after login
            else:
                error = 'Invalid username or password. Please try again.'
                return render_template('login.html', error=error)
        except sqlite3.Error as e:
            print("SQLite error:", e)
            error = 'An error occurred. Please try again later.'
            return render_template('login.html', error=error)
        finally:
            conn.close()
    return render_template('login.html')

# Route for registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            error = 'Passwords do not match. Please try again.'
            return render_template('register.html', error=error)
        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            return redirect('/login')  # Redirect to login page after successful registration
        except sqlite3.IntegrityError as e:
            print("SQLite integrity error:", e)
            error = 'Username already exists. Please choose a different username.'
            return render_template('register.html', error=error)
        except sqlite3.Error as e:
            print("SQLite error:", e)
            error = 'An error occurred. Please try again later.'
            return render_template('register.html', error=error)
        finally:
            conn.close()
    return render_template('register.html')

# Route for logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

# Route for index page (login required)
@app.route('/')
def index():
    """Video streaming home page."""
    if 'username' not in session:
        return redirect('/login')
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (session['username'],)).fetchone()
    conn.close()
    
    if user:
        return render_template('index.html', user=user)
    else:
        return "User not found."  # Handle this case appropriately

# Route for starting drowsiness detection
@app.route('/start', methods=["POST"])
def start():
    """Start drowsiness detection."""
    if 'username' not in session:
        return redirect('/login')
    webcam = Camera()
    webcam.set_classifier(1)
    timestamp = datetime.datetime.now()
    webcam.set_time_start(timestamp)
    return "Classifier ON - Status {0}\n Time Start: {1}".format(webcam.classifier, timestamp)

# Route for stopping drowsiness detection
@app.route('/stop', methods=["POST"])
def stop():
    """Stop drowsiness detection."""
    if 'username' not in session:
        return redirect('/login')

    webcam.set_classifier(0)
    final = webcam.get_score()
    timestamp = datetime.datetime.now()
    webcam.set_time_end(timestamp)
    duration = webcam.get_duration()
    webcam.camera_reset()
    if final == 100:
        try:
            playthread = threading.Thread(target=start_player, args=(perfect,) )
            playthread.start()
        except Exception as e:
            print(e)
        
    points = duration * 10 * final/10
    print(points)
    return "Final Score: {0}\n Duration: {1} \n Total Points: {2}".format(final,duration, points)

# Route for restarting camera
@app.route('/restart', methods=['POST'])
def restart():
    """Restart camera."""
    if 'username' not in session:
        return redirect('/login')

    webcam = Camera()
    return "Camera restarted"

# Route for video feed (login required)
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    if 'username' not in session:
        return redirect('/login')
    
    return Response(response=gen(webcam), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    init_gui(app, port=5000, width=640, height=800, window_title="DROWZEE", icon=icon, argv=None)