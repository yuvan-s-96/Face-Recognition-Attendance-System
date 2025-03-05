import React, { useState, useEffect } from 'react';
import '../styles/face.css';
const FaceRecognition = () => {
  const [attendanceData, setAttendanceData] = useState([]);

  useEffect(() => {
    const fetchAttendance = async () => {
      const response = await fetch('http://localhost:5000/attendance');
      const data = await response.json();
      setAttendanceData(data);
    };

    fetchAttendance();
    const interval = setInterval(fetchAttendance, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container">
      <h1>Face Recognition Attendance System</h1>
      <div className="flex">
        <div className="w-2/3">
          <h2>Live Video Feed</h2>
          <img src="http://localhost:5000/video_feed" alt="Video feed" />
        </div>
        <div className="w-1/3">
          <h2>Attendance List</h2>
          <ul>
            {attendanceData.map((entry, index) => (
              <li key={index}>
                <span>{entry.name}</span>: {entry.time}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default FaceRecognition;
