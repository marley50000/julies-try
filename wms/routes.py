from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from wms import db
import datetime

from wms.models import User, Task, Shift, Attendance, LeaveRequest
from wms.forms import RegistrationForm, LoginForm, TaskForm, ShiftForm, LeaveRequestForm, EmptyForm
from .decorators import roles_required

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
@main_bp.route("/home")
@login_required
def home():
    tasks = current_user.tasks_assigned_to
    shifts = current_user.shifts
    last_attendance = Attendance.query.filter_by(user_id=current_user.id).order_by(Attendance.clock_in_time.desc()).first()
    attendance_history = Attendance.query.filter_by(user_id=current_user.id).order_by(Attendance.clock_in_time.desc()).limit(7).all()
    leave_requests = current_user.leave_requests
    clock_form = EmptyForm()
    return render_template('index.html', title='Home', tasks=tasks, shifts=shifts, last_attendance=last_attendance, attendance_history=attendance_history, leave_requests=leave_requests, clock_form=clock_form)

@main_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main_bp.route("/task/new", methods=['GET', 'POST'])
@login_required
@roles_required('Admin', 'Manager')
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data,
                    description=form.description.data,
                    priority=form.priority.data,
                    deadline=form.deadline.data,
                    assigned_to=form.assigned_to.data,
                    assigned_by=current_user)
        db.session.add(task)
        db.session.commit()
        flash('The task has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_task.html', title='New Task', form=form, legend='New Task')


@main_bp.route("/shift/new", methods=['GET', 'POST'])
@login_required
@roles_required('Admin', 'Manager')
def new_shift():
    form = ShiftForm()
    if form.validate_on_submit():
        shift = Shift(start_time=form.start_time.data,
                      end_time=form.end_time.data,
                      user=form.user.data)
        db.session.add(shift)
        db.session.commit()
        flash('The shift has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_shift.html', title='New Shift', form=form, legend='New Shift')


@main_bp.route("/attendance/clock", methods=['POST'])
@login_required
def clock_in_out():
    last_attendance = Attendance.query.filter_by(user_id=current_user.id).order_by(Attendance.clock_in_time.desc()).first()

    if last_attendance and last_attendance.clock_out_time is None:
        # Clock out
        last_attendance.clock_out_time = datetime.datetime.utcnow()
        flash('You have been clocked out.', 'success')
    else:
        # Clock in
        new_attendance = Attendance(user_id=current_user.id)
        db.session.add(new_attendance)
        flash('You have been clocked in.', 'success')

    db.session.commit()
    return redirect(url_for('main.home'))


@main_bp.route("/leave/new", methods=['GET', 'POST'])
@login_required
def new_leave_request():
    form = LeaveRequestForm()
    if form.validate_on_submit():
        leave_request = LeaveRequest(start_date=form.start_date.data,
                                     end_date=form.end_date.data,
                                     reason=form.reason.data,
                                     user=current_user)
        db.session.add(leave_request)
        db.session.commit()
        flash('Your leave request has been submitted.', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_leave_request.html', title='New Leave Request', form=form, legend='New Leave Request')


@main_bp.route("/leave/requests")
@login_required
@roles_required('Admin', 'Manager')
def leave_requests():
    requests = LeaveRequest.query.order_by(LeaveRequest.start_date.asc()).all()
    return render_template('leave_requests.html', title='Leave Requests', requests=requests)


@main_bp.route("/leave/requests/<int:request_id>/approve", methods=['POST'])
@login_required
@roles_required('Admin', 'Manager')
def approve_leave_request(request_id):
    leave_request = LeaveRequest.query.get_or_404(request_id)
    leave_request.status = 'Approved'
    db.session.commit()
    flash('The leave request has been approved.', 'success')
    return redirect(url_for('main.leave_requests'))


@main_bp.route("/leave/requests/<int:request_id>/reject", methods=['POST'])
@login_required
@roles_required('Admin', 'Manager')
def reject_leave_request(request_id):
    leave_request = LeaveRequest.query.get_or_404(request_id)
    leave_request.status = 'Rejected'
    db.session.commit()
    flash('The leave request has been rejected.', 'danger')
    return redirect(url_for('main.leave_requests'))
