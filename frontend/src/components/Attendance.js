import React, { useState } from 'react';
import axios from 'axios';
import '../styles/attendance.css'; 

function App() {
  const [selectedDate, setSelectedDate] = useState('');
  const [attendanceData, setAttendanceData] = useState([]);
  const [error, setError] = useState('');

  const handleDateChange = (e) => {
    setSelectedDate(e.target.value);
  };

  const fetchAttendance = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/api/attendance?date=${selectedDate}`);
      setAttendanceData(response.data);
      setError('');
    } catch (error) {
      setAttendanceData([]);
      setError(error.response?.data?.error || 'An error occurred while fetching the attendance');
    }
  };

  const downloadReport = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/api/report?date=${selectedDate}`, {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `attendance_report_${selectedDate}.xlsx`);
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      setError(error.response?.data?.error || 'An error occurred while downloading the report');
    }
  };

  return (
    <div>
      <div className="App">
        <h1>Attendance Tracker</h1>
        <div>
          <input type="date" value={selectedDate} onChange={handleDateChange} />
          <button onClick={fetchAttendance}>Get Attendance</button>
          <button onClick={downloadReport}>Download Report</button>
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {attendanceData.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Time</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {attendanceData.map((item, index) => (
                <tr key={index} style={{ backgroundColor: getStatusColor(item.status) }}>
                  <td>{item.name}</td>
                  <td>{item.time}</td>
                  <td>{item.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

// Function to set background color based on status
const getStatusColor = (status) => {
  if (status === 'Latecomer') return '#FFA500';  // Orange
  if (status === 'Absent') return '#FF0000';  // Red
  if (status === 'Present') return '#C6EFCE';  // Green
  return 'inherit';
};

export default App;
