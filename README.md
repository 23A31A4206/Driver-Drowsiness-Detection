Smart Driver Drowsiness Detection & Alert System

Overview

This project is a real-time Driver Drowsiness Detection and Alert System developed using Python, OpenCV, and MediaPipe.

The system monitors the driver's eyes through a webcam and detects signs of drowsiness. When the driver's eyes remain closed for a certain period, the system triggers an alert sound and provides safety warnings to help prevent accidents caused by fatigue.

# How It Works
1. Captures live video from the webcam.
2. Detects facial landmarks using MediaPipe Face Mesh.
3. Monitors eye closure duration.
4. Triggers an alert if eyes remain closed for more than 2 seconds.
5. Increases the drowsiness event count.
6. Updates the driver safety score.
7. Provides voice alerts when fatigue levels become critical.

# Features
* Real-Time Face Detection
* Driver Face Bounding Box
* Eye Closure Detection
* Drowsiness Alert Sound
* Drowsiness Event Counter
* Driver Safety Score Monitoring
* Voice Alert for Break Recommendation
* Critical Fatigue Warning System
* Real-Time Monitoring using Webcam

# Technologies Used
* Python
* OpenCV
* MediaPipe
* Pyttsx3
* Winsound

# Project Structure

Driver-Drowsiness-Detection

├── app.py

├── README.md

└── .vscode/

Developed by 

Illa Lakshmi Siri Siva Sai Chandana 
B.Tech (Artificial Intelligence & Machine Learning)
GitHub: https://github.com/23A31A4206
