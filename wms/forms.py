from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.fields import DateField
from wtforms.validators import Optional
from flask_wtf.file import FileField, FileAllowed
from wms.models import User, Document

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


def user_query():
    return User.query


class DocumentForm(FlaskForm):
    file = FileField('Document', validators=[DataRequired(), FileAllowed(['pdf', 'doc', 'docx', 'jpg', 'png'])])
    user = QuerySelectField('Employee', query_factory=user_query, get_label='username', allow_blank=False,
                            validators=[DataRequired()])
    category = SelectField('Category', choices=[('General', 'General'), ('Payslip', 'Payslip'), ('Contract', 'Contract')],
                           validators=[DataRequired()])
    expiry_date = DateField('Expiry Date (Optional)', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Upload Document')