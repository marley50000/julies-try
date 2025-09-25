from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from wms import db
import datetime
import os

from wms.models import User, Document
from wms.forms import RegistrationForm, LoginForm, DocumentForm
from .decorators import roles_required
from werkzeug.utils import secure_filename
from flask import current_app

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
@main_bp.route("/home")
@login_required
def home():
    return render_template('home.html', title='Home')

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


@main_bp.route("/document/upload", methods=['GET', 'POST'])
@login_required
@roles_required('Admin', 'Manager')
def upload_document():
    form = DocumentForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        document = Document(filename=filename,
                              user=form.user.data,
                              category=form.category.data,
                              expiry_date=form.expiry_date.data)
        db.session.add(document)
        db.session.commit()
        flash('The document has been uploaded.', 'success')
        return redirect(url_for('main.documents'))
    return render_template('upload_document.html', title='Upload Document', form=form)


@main_bp.route("/documents")
@login_required
@roles_required('Admin', 'Manager')
def documents():
    query = request.args.get('q')
    if query:
        docs = Document.query.filter(Document.filename.contains(query)).all()
    else:
        docs = Document.query.all()
    return render_template('documents.html', title='Document Management', documents=docs, today=datetime.date.today())


@main_bp.route("/my_payslips")
@login_required
def my_payslips():
    payslips = Document.query.filter_by(user=current_user, category='Payslip').order_by(Document.upload_date.desc()).all()
    return render_template('my_payslips.html', title='My Payslips', payslips=payslips)