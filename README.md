# Workout Rep Tracker
A Python application that uses a webcam to track body joints, counts exercise reps live, and saves workout history to a SQL database.

## Demo & Dashboard
![Tracker Demo](docs/[your_demo_file_name].gif)
![Dashboard](docs/[your_screenshot_name].png)

## Features
* Live webcam tracking of one person using MediaPipe pose detection.
* Real-time rep counting for squats, bicep curls, and push-ups with an on-screen overlay.
* Saves finished sessions (exercise, reps, duration, date) to a SQLite database.
* A Flask REST API and web dashboard showing session history, totals, and a reps-per-day chart.

## Tech Stack
* **Language:** Python 3.10+
* **Video & Vision:** OpenCV (opencv-python), MediaPipe Pose
* **Database:** SQLite (sqlite3)
* **Backend:** Flask
* **Frontend:** HTML, CSS, vanilla JavaScript, Chart.js
* **Testing:** pytest

## Setup & Execution
1. Clone the repository and navigate to the project directory.
2. Create and activate a virtual environment:
   `python -m venv .venv`
   `source .venv/bin/activate` (or `.\.venv\Scripts\activate` on Windows)
3. Install dependencies:
   `pip install -r requirements.txt`
4. Run the live tracker:
   `python run_tracker.py --exercise squat`
5. Run the web server (dashboard available at http://127.0.0.1:5000):
   `python run_server.py`

## How Rep Counting Works
The core logic relies on measuring the angle between three body landmarks (e.g., hip, knee, and ankle for squats)[cite: 1]. A state machine monitors this angle, waiting for it to pass an "extended" threshold, drop below a "flexed" threshold, and return to extended[cite: 1]. This complete cycle registers as one valid rep, preventing double-counting from minor jitter[cite: 1].

## Project Structure
```text
workout-rep-tracker/
├── app/
│   ├── __init__.py
│   ├── angles.py        # Pure math: angle between three points
│   ├── counter.py       # Exercise config + RepCounter state machine
│   ├── tracker.py       # Webcam loop, pose detection, overlay
│   ├── db.py            # SQLite database logic
│   └── server.py        # Flask app and API routes
├── templates/
│   └── index.html       # Dashboard page
├── static/
│   ├── style.css
│   └── app.js
├── tests/
│   ├── test_angles.py
│   ├── test_counter.py
│   ├── test_db.py
│   └── test_api.py
├── data/                # SQLite file (gitignored)
├── docs/                # demo.gif and screenshots
├── run_tracker.py       # Entry point for tracker
├── run_server.py        # Entry point for server
├── requirements.txt
├── .gitignore
└── README.md