import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage';
import AboutPage from './components/AboutPage'; 
// import VideoDeepfake from './components/VideoDeepfake';
import FaceAttendance from './components/Face';
import AttendanceTracker from './components/Attendance';
import ContactPage from './components/ContactPage';

const App = () => {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/face-attendance" element={<FaceAttendance />} />
          <Route path="/attendance-tracker" element={<AttendanceTracker/>} />
          <Route path="/contact" element={<ContactPage/>} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
