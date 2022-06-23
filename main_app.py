from flask import Flask, Response, redirect, render_template, url_for
from face_rec import generate_frame, mark_attendance, face_detected
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/face_recognition_project'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    
db = SQLAlchemy(app)

detected_face = ''

class Student(db.Model):
    univ_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(30),nullable=False)
    attendance = db.Column(db.Integer,default=0)
    dob = db.Column(db.DateTime,nullable=True)
    gen = db.Column(db.String(2), nullable=False)
    ph_no = db.Column(db.String(10),nullable=False)
    course = db.Column(db.String(20), nullable=False)
    sem = db.Column(db.Integer,nullable=False)
    sec = db.Column(db.String(2),nullable=False)
    croll_no = db.Column(db.Integer,nullable=False)

    def __repr__(self) -> str:
        return f'{self.univ_id} - {self.name}'

@app.route('/')
def index():
    return render_template('face_detect.html')

@app.route('/video')
def video():
    return Response(generate_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detect')
def detect():
    global detected_face
    print("Face Detected : ",face_detected())
    stu_details = ''
    detected_face = face_detected()
    if detected_face != '':
        print("no im here")
        stu_details = Student.query.filter_by(univ_id=detected_face).first()
        print(stu_details)
        return render_template('profile.html',stu_details = stu_details)
    else:
        print("Im here")
        # return Response()
        # return redirect(url_for('index'))
        return render_template('face_detect.html', noface = True)
        # return render_template('profile.html',stu_details = stu_details)
        

@app.route('/mark')
def mark():
    print(detected_face)
    res = mark_attendance(detected_face)
    # curr_student = ''
    curr_student = Student.query.filter_by(univ_id=face_detected()).first()
    if res == 1:
        curr_student.attendance = curr_student.attendance + 1
        db.session.commit()
        # return "attendance marked"
        return render_template('profile.html', stu_details = curr_student, status = res)
    else:
        # return "attendance already marked"
        return render_template('profile.html', stu_details = curr_student, status = res)

if __name__ == '__main__':
    app.run(debug=True)