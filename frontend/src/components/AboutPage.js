import React from 'react';
import '../styles/About.css'; // Make sure to create this CSS file for styling

const About = () => {
    return (
        <div className="about-container">
            <h1>About the Face Recognition Attendance System</h1>
            <p>Welcome to our Face Recognition Attendance System! This application is designed to automate the process of tracking attendance using advanced face recognition technology. Here's an overview of the system and how it works:</p>
            
            <h2>Technology Stack</h2>
            <ul>
                <li><strong>Python</strong> - The core programming language used for implementing the face recognition and attendance tracking features.</li>
                <li><strong>OpenCV</strong> - A computer vision library used for capturing video from the camera and processing images.</li>
                <li><strong>dlib</strong> - A toolkit used for face detection and recognition, including facial landmark detection and face descriptor extraction.</li>
                <li><strong>Flask</strong> - A lightweight web framework used to build the RESTful API and serve the web application.</li>
                <li><strong>SQLite</strong> - A database system used to store attendance records.</li>
                <li><strong>Pandas</strong> - A data manipulation library used to handle and generate reports in Excel format.</li>
            </ul>

            <h2>Features</h2>
            <ul>
                <li><strong>Real-Time Face Detection:</strong> The system captures live video feed and detects faces in real-time using dlib's face detector.</li>
                <li><strong>Face Recognition:</strong> Recognizes known faces based on pre-stored face features and records attendance.</li>
                <li><strong>Attendance Management:</strong> Records and manages attendance data in a SQLite database with date and time stamps.</li>
                <li><strong>Data Filtering:</strong> Allows filtering of attendance data based on specific time conditions (e.g., after 9 AM).</li>
                <li><strong>Report Generation:</strong> Generates downloadable attendance reports in Excel format, highlighting latecomers and present attendees.</li>
            </ul>

            <h2>How It Works</h2>
            <p>The system operates in the following steps:</p>
            <ol>
                <li><strong>Video Capture:</strong> Captures live video from the camera and processes each frame to detect faces.</li>
                <li><strong>Face Processing:</strong> Extracts facial landmarks and features from detected faces.</li>
                <li><strong>Face Recognition:</strong> Matches the extracted features with known faces from the database to identify individuals.</li>
                <li><strong>Attendance Logging:</strong> Logs the attendance of recognized individuals into the database.</li>
                <li><strong>Report Generation:</strong> Provides options to view and download attendance reports filtered by date and time.</li>
            </ol>

            <h2>Contact Us</h2>
            <p>If you have any questions or need further information about the system, feel free to contact us at <a href="mailto:support@example.com">support@example.com</a>.</p>
        </div>
    );
};

export default About;
