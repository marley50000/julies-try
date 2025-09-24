from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from wms import db
from wms.models import User, Task, Shift
from wms.forms import RegistrationForm, LoginForm, TaskForm, ShiftForm
from .decorators import roles_required

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
@main_bp.route("/home")
@login_required
def home():
    tasks = current_user.tasks_assigned_to
    shifts = current_user.shifts
    return render_template('index.html', title='Home', tasks=tasks, shifts=shifts)

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
