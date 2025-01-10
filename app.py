from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import cv2
import dlib
import numpy as np
import os
import pickle

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)

# Ensure the database is created before the app starts
@app.before_request
def setup_database():
    with app.app_context():
        db.create_all()

# Dlib face detector and face descriptor
detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# Known faces folder
KNOWN_FACES_DIR = "known_faces"
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

# Employee model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer)
    job_role = db.Column(db.String(120))
    team = db.Column(db.String(120))
    face_encoding = db.Column(db.PickleType, nullable=False)
    attendance = db.Column(db.PickleType, default={})  # To store attendance data

# Admin face encoding storage model (separate from Employee for admin-specific purposes)
class AdminFaceEncoding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encoding = db.Column(db.PickleType, nullable=False)

# Helper function to encode face
def encode_face(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    if len(faces) == 0:
        return None
    shape = shape_predictor(gray, faces[0])
    face_descriptor = np.array(face_rec_model.compute_face_descriptor(image, shape))
    return face_descriptor

# Route to home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Admin verification
        admin_verified = False

        # Load admin's face encoding from the database
        admin_face_encoding = AdminFaceEncoding.query.first()
        if admin_face_encoding is None:
            return "Error: Admin's face encoding not found. Please ensure admin is registered properly."
        
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Ensure using DirectShow
        if not cap.isOpened():
            return "Error: Unable to access the webcam."
        
        while not admin_verified:
            ret, frame = cap.read()
            if not ret:
                return "Error: Unable to capture a frame."
            
            face_encoding = encode_face(frame)
            if face_encoding is None:
                return "Face detection failed. Try again."

            # Compare the captured face with the admin's face encoding
            if np.linalg.norm(np.array(admin_face_encoding.encoding) - face_encoding) < 0.6:
                admin_verified = True
                break

        cap.release()
        cv2.destroyAllWindows()

        if admin_verified:
            name = request.form['name']
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not cap.isOpened():
                return "Error: Unable to access the webcam."
            
            ret, frame = cap.read()
            if not ret:
                return "Error: Unable to capture a frame."
            face_encoding = encode_face(frame)
            if face_encoding is None:
                return "Face capture failed. Try again."
            
            new_employee = Employee(name=name, face_encoding=face_encoding)
            db.session.add(new_employee)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return "Admin Verification Failed."
    return render_template('register.html')

# Route to login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        cv2.destroyAllWindows()
        if not ret:
            return "Camera not working."
        face_encoding = encode_face(frame)
        if face_encoding is None:
            return "No face detected."
        for employee in Employee.query.all():
            if np.linalg.norm(np.array(employee.face_encoding) - face_encoding) < 0.6:
                session['employee_id'] = employee.id
                return redirect(url_for('dashboard'))
        return "Not Registered. Please Register to Login."
    return render_template('login.html')

# Route to dashboard page
@app.route('/dashboard')
def dashboard():
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    employee = Employee.query.get(session['employee_id'])
    return render_template('dashboard.html', employee=employee)

# Route to update employee details
@app.route('/update_details', methods=['GET', 'POST'])
def update_details():
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    employee = Employee.query.get(session['employee_id'])
    if request.method == 'POST':
        employee.name = request.form['name']
        employee.age = request.form['age']
        employee.job_role = request.form['job_role']
        employee.team = request.form['team']
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('update_details.html', employee=employee)

# Route to update employee photo
@app.route('/photo_update', methods=['POST'])
def photo_update():
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()
    if not ret:
        return "Camera not working."
    face_encoding = encode_face(frame)
    if face_encoding is None:
        return "No face detected."
    employee = Employee.query.get(session['employee_id'])
    employee.face_encoding = face_encoding
    db.session.commit()
    return redirect(url_for('dashboard'))

# Route to logout page
@app.route('/logout')
def logout():
    session.pop('employee_id', None)
    return redirect(url_for('index'))

# Admin face encoding setup route
@app.route('/setup_admin', methods=['GET', 'POST'])
def setup_admin():
    if request.method == 'POST':
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            return "Error: Unable to access the webcam."
        
        ret, frame = cap.read()
        cap.release()
        cv2.destroyAllWindows()
        if not ret:
            return "Error: Unable to capture frame."
        
        face_encoding = encode_face(frame)
        if face_encoding is None:
            return "No face detected"

        # Save admin face encoding to the database
        admin_face = AdminFaceEncoding(encoding=face_encoding)
        db.session.add(admin_face)
        db.session.commit()
        return "Admin face encoding has been saved."
    
    return render_template('setup_admin.html')

if __name__ == '__main__':
    app.run(debug=True)
