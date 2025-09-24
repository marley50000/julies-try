from wms import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from sqlalchemy import Text, Date


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(50), nullable=False, default='Employee') # Roles: Admin, Manager, Employee

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(Text, nullable=True)
    priority = db.Column(db.String(20), nullable=False, default='Medium')  # Low, Medium, High
    deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='To Do')  # To Do, In Progress, Done
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id], backref='tasks_assigned_to')
    assigned_by = db.relationship('User', foreign_keys=[assigned_by_id], backref='tasks_created_by')

    def __repr__(self):
        return f"Task('{self.title}', '{self.status}')"


class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='shifts')

    def __repr__(self):
        return f"Shift('{self.user.username}', '{self.start_time}' to '{self.end_time}')"


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clock_in_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    clock_out_time = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='attendances')

    def __repr__(self):
        return f"Attendance('{self.user.username}', '{self.clock_in_time}')"


class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(Date, nullable=False)
    end_date = db.Column(Date, nullable=False)
    reason = db.Column(Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')  # Pending, Approved, Rejected
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='leave_requests')

    def __repr__(self):
        return f"LeaveRequest('{self.user.username}', '{self.start_date}' to '{self.end_date}')"


class Salary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    basic_pay = db.Column(db.Float, nullable=False, default=0.0)
    allowances = db.Column(db.Float, nullable=False, default=0.0)
    deductions = db.Column(db.Float, nullable=False, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('salary', uselist=False))

    def __repr__(self):
        return f"Salary('{self.user.username}', '{self.basic_pay}')"
