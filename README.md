# Face Recognition-Based Attendance System

## Overview
This project is a face recognition-based attendance tracking system that utilizes deep learning models for face detection and recognition. The system captures real-time video input, recognizes faces using dlib's face recognition model, and records attendance in a database. A Flask-based backend handles data storage and retrieval, while the frontend, built with React, allows users to interact with the system.

## Features
- **Face Registration:** Users can register their faces through a GUI-based interface.
- **Feature Extraction:** Extracts 128D face descriptors and stores them in a CSV file.
- **Real-Time Face Recognition:** Recognizes registered faces from a video stream.
- **Attendance Logging:** Stores attendance records in an SQLite database.
- **Latecomer & Absentee Tracking:** Flags latecomers and absentees based on predefined time constraints.
- **Report Generation:** Allows users to download attendance reports in Excel format.
- **Web-Based Access:** A Flask backend serves attendance data to a React frontend.

## System Requirements
- Python 3.7+
- Node.js (for the React frontend)

## Installation & Setup
### 1. Clone the Repository
```sh
git clone <repository_link>
cd <repository_name>
```

### 2. Set Up the Backend
#### Install Dependencies
Navigate to the project root (where `requirements.txt` is located) and install the required Python packages:
```sh
pip install -r requirements.txt
```

#### Initialize Database
Run the following command to create the SQLite database and necessary tables:
```sh
python attendance_taker.py
```

#### Start the Backend Server
```sh
python app1.py
```
This starts the Flask backend on `http://localhost:5000/`.

### 3. Set Up the Frontend
Navigate to the `frontend` directory:
```sh
cd frontend
```
Install dependencies:
```sh
npm install
```
Run the frontend development server:
```sh
npm start
```
This launches the React frontend at `http://localhost:3000/`.

## Usage
1. **Register Faces**
   - Run `get_faces_from_camera_tkinter.py` to capture face images.
   - Input the person's name and save images.

2. **Extract Features**
   - Run `features_extraction_to_csv.py` to generate the `features_all.csv` file.

3. **Start Attendance Tracking**
   - Run `app1.py` to start face recognition and attendance marking.
   - Open the React frontend to view attendance records.

4. **Generate Reports**
   - Navigate to the frontend and select a date to download the attendance report.

## State-of-the-Art Technologies Used
- **Face Recognition:** Uses dlib’s ResNet-based face recognition model for high accuracy.
- **Deep Learning:** Leverages pre-trained deep learning models for feature extraction.
- **Computer Vision:** Uses OpenCV for real-time face detection and tracking.
- **Web Technologies:** Implements Flask for the backend API and React for the frontend UI.
- **Database Management:** Uses SQLite for attendance tracking and report generation.

## Future Enhancements
- **Cloud Integration:** Storing attendance records on a cloud database for remote access.
- **Enhanced Security:** Adding anti-spoofing techniques to prevent fraud.
- **Mobile App:** Creating a mobile application for easier attendance marking.

## Contributors
- [Yuvan Velkumar]
- [Navin]
- [Sujith]
- [Vishal]



