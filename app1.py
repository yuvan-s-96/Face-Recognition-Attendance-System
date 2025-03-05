import cv2
import dlib
import numpy as np
import pandas as pd
import time
import logging
import sqlite3
import datetime
from flask import Flask, Response, jsonify, request, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Dlib setup
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('data_dlib/shape_predictor_68_face_landmarks.dat')
face_reco_model = dlib.face_recognition_model_v1("data_dlib/dlib_face_recognition_resnet_model_v1.dat")

# Database setup
conn = sqlite3.connect("attendance.db", check_same_thread=False)
cursor = conn.cursor()

# Create attendance table
current_date = datetime.datetime.now().strftime("%Y_%m_%d")
table_name = "attendance"
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    name TEXT,
    time TEXT,
    date DATE,
    status TEXT,
    UNIQUE(name, date)
)"""
cursor.execute(create_table_sql)

# Create latecomer_count table
create_latecomer_count_sql = """
CREATE TABLE IF NOT EXISTS latecomer_count (
    name TEXT PRIMARY KEY,
    count INTEGER DEFAULT 0,
    last_updated DATE
)"""
cursor.execute(create_latecomer_count_sql)

# Create absent_count table
create_absent_count_sql = """
CREATE TABLE IF NOT EXISTS absent_count (
    name TEXT PRIMARY KEY,
    count INTEGER DEFAULT 0,
    last_updated DATE
)"""
cursor.execute(create_absent_count_sql)

conn.commit()

class FaceRecognizer:
    def __init__(self):
        self.face_features_known_list = []
        self.face_name_known_list = []
        self.current_frame_face_cnt = 0
        self.current_frame_face_name_list = []
        self.get_face_database()

    def get_face_database(self):
        if os.path.exists("data/features_all.csv"):
            csv_rd = pd.read_csv("data/features_all.csv", header=None)
            for i in range(csv_rd.shape[0]):
                self.face_name_known_list.append(csv_rd.iloc[i][0])
                self.face_features_known_list.append([float(x) for x in csv_rd.iloc[i][1:]])
            logging.info("Faces in Database: %d", len(self.face_features_known_list))
        else:
            logging.warning("'features_all.csv' not found!")

    @staticmethod
    def return_euclidean_distance(feature_1, feature_2):
        return np.linalg.norm(np.array(feature_1) - np.array(feature_2))

    def recognize_face(self, face_feature):
        e_distance_list = []
        for i in range(len(self.face_features_known_list)):
            e_distance_list.append(self.return_euclidean_distance(face_feature, self.face_features_known_list[i]))
        similar_person_num = e_distance_list.index(min(e_distance_list))
        if min(e_distance_list) < 0.4:
            return self.face_name_known_list[similar_person_num]
        else:
            return "Unknown"

    def attendance(self, name):
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        
        status = self.get_status(current_time)
        
        cursor.execute("SELECT * FROM attendance WHERE name = ? AND date = ?", (name, current_date))
        existing_entry = cursor.fetchone()
        if not existing_entry:
            cursor.execute("INSERT INTO attendance (name, time, date, status) VALUES (?, ?, ?, ?)", 
                           (name, current_time, current_date, status))
            conn.commit()
            logging.info(f"{name} marked as {status} for {current_date} at {current_time}")
            
            if status == 'Latecomer':
                self.update_latecomer_count(name, current_date)
            elif status == 'Absent':
                self.update_absent_count(name, current_date)

    def get_status(self, time):
        if '08:15:00' <= time <= '08:45:00' or '13:20:00' <= time <= '14:00:00':
            return 'Present'
        elif '08:45:00' < time < '09:30:00' or '14:00:00' < time < '14:30:00':
            return 'Latecomer'
        elif '09:30:00' <= time or '14:30:00' <= time:
            return 'Absent'
        return 'On Time'

    def update_latecomer_count(self, name, current_date):
        cursor.execute("SELECT count, last_updated FROM latecomer_count WHERE name = ?", (name,))
        result = cursor.fetchone()
        
        if result:
            count, last_updated = result
            if last_updated != current_date:
                count += 1
                cursor.execute("UPDATE latecomer_count SET count = ?, last_updated = ? WHERE name = ?", 
                               (count, current_date, name))
        else:
            count = 1
            cursor.execute("INSERT INTO latecomer_count (name, count, last_updated) VALUES (?, ?, ?)", 
                           (name, count, current_date))
        
        conn.commit()
        
        if count >= 3:
            self.send_message(name, "latecomer")

    def update_absent_count(self, name, current_date):
        cursor.execute("SELECT count, last_updated FROM absent_count WHERE name = ?", (name,))
        result = cursor.fetchone()
        
        if result:
            count, last_updated = result
            if last_updated != current_date:
                count += 1
                cursor.execute("UPDATE absent_count SET count = ?, last_updated = ? WHERE name = ?", 
                               (count, current_date, name))
        else:
            count = 1
            cursor.execute("INSERT INTO absent_count (name, count, last_updated) VALUES (?, ?, ?)", 
                           (name, count, current_date))
        
        conn.commit()
        
        if count > 4:
            self.send_message(name, "absent")

    def send_message(self, name, reason):
        if reason == "latecomer":
            logging.warning(f"Message sent: Student {name} has been late for 3 or more days.")
        elif reason == "absent":
            logging.warning(f"Message sent: Student {name} has been absent for more than 4 days.")
        # Here you would implement the actual logic to send a message to the concerned authority
        # This could involve sending an email, SMS, or using some other notification system

    def process_frame(self, frame):
        faces = detector(frame, 0)
        self.current_frame_face_cnt = len(faces)
        self.current_frame_face_name_list = []

        for face in faces:
            shape = predictor(frame, face)
            face_descriptor = face_reco_model.compute_face_descriptor(frame, shape)
            name = self.recognize_face(face_descriptor)
            self.current_frame_face_name_list.append(name)
            if name != "Unknown":
                self.attendance(name)

            cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 2)
            cv2.putText(frame, name, (face.left(), face.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        return frame

face_recognizer = FaceRecognizer()

def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = face_recognizer.process_frame(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    selected_date = request.args.get('date')
    selected_time_filter = request.args.get('time_filter')

    if not selected_date:
        return jsonify({"error": "Please select a date."}), 400

    try:
        selected_date_obj = datetime.datetime.strptime(selected_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Please select a valid date."}), 400

    formatted_date = selected_date_obj.strftime('%Y-%m-%d')

    cursor.execute("SELECT name, time, status FROM attendance WHERE date = ?", (formatted_date,))
    attendance_data = cursor.fetchall()

    if not attendance_data:
        return jsonify({"error": "No data available for the selected date."}), 404

    # Apply time filter
    filtered_data = []
    for name, time, status in attendance_data:
        highlight = 'No'
        if selected_time_filter == 'after_9am' and time >= '09:00:00':
            highlight = 'Yes'
        elif selected_time_filter == 'after_2pm' and time >= '14:00:00':
            highlight = 'Yes'
        filtered_data.append({"name": name, "time": time, "status": status, "highlight": highlight})

    return jsonify(filtered_data)

@app.route('/api/download_report', methods=['GET'])
def download_report():
    selected_date = request.args.get('date')

    if not selected_date:
        return jsonify({"error": "Please select a date."}), 400

    try:
        selected_date_obj = datetime.datetime.strptime(selected_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Please select a valid date."}), 400

    formatted_date = selected_date_obj.strftime('%Y-%m-%d')

    cursor.execute("SELECT name, time, status FROM attendance WHERE date = ?", (formatted_date,))
    attendance_data = cursor.fetchall()

    if not attendance_data:
        return jsonify({"error": "No data available for the selected date."}), 404

    # Convert to DataFrame
    df = pd.DataFrame(attendance_data, columns=['RollNo', 'Time', 'Status'])

    # Create Excel file with date in the filename
    filename = f'attendance_{formatted_date}.xlsx'
    output = pd.ExcelWriter(filename, engine='xlsxwriter')
    df.to_excel(output, index=False, sheet_name='Attendance')

    workbook = output.book
    worksheet = output.sheets['Attendance']

    # Define formats
    latecomer_format = workbook.add_format({'bg_color': '#FFA500', 'font_color': '#000000'})  # Orange
    absent_format = workbook.add_format({'bg_color': '#FF0000', 'font_color': '#FFFFFF'})  # Red
    present_format = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})  # Green
    
    # Apply conditional formatting
    worksheet.conditional_format('C2:C{}'.format(len(df) + 1), 
                                  {'type': 'text',
                                   'criteria': 'containing',
                                   'value': 'Latecomer',
                                   'format': latecomer_format})
    worksheet.conditional_format('C2:C{}'.format(len(df) + 1), 
                                  {'type': 'text',
                                   'criteria': 'containing',
                                   'value': 'Absent',
                                   'format': absent_format})
    worksheet.conditional_format('C2:C{}'.format(len(df) + 1), 
                                  {'type': 'text',
                                   'criteria': 'containing',
                                   'value': 'Present',
                                   'format': present_format})

    output.close()

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)