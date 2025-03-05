import React, { useState } from 'react';
import Navbar from './NavBar'; 
import Copyright from './CopyRight'; // Corrected import path
import '../styles/Homepage.css'; // Corrected import path
import Carousel from './Carousel'; // Import the Carousel component

const HomePage = () => {
  const [showSignIn, setShowSignIn] = useState(true); // State to toggle between login and sign-up forms

  return (
    <div>
      <Navbar />
      <div className="homepage-content">
        <h1 className="homepage-title">Welcome to the Future of Attendance</h1>
        <p className="homepage-description">
          Harness the power of face recognition technology to simplify attendance tracking. Our system ensures secure, efficient, and real-time monitoring with anomaly detection for better management.
        </p>
        <div className="homepage-highlight">
          <p>
            Revolutionize your attendance process with:
            <ul>
              <li>Instant face recognition</li>
              <li>Accurate anomaly detection</li>
              <li>Real-time data processing</li>
            </ul>
          </p>
        </div>
        <Carousel />

        
        
        
        <Copyright />
      </div>
    </div>
  );
};

export default HomePage;
