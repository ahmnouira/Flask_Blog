from flask_wtf import FlaskForm                                               # import FlaskForm from flask_wtf package
from wtforms import StringField, PasswordField, BooleanField, SubmitField     # import Fields
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo  # to check the required fields,
from wtforms import TextAreaField                                             # import TextAreaFiled
from wtforms.validators import Length                                         # import Length
from app.models import User


class LoginForm(FlaskForm):    # create LoginForm class
    username = StringField('Email address(text!):', validators=[DataRequired()])  # field required, type String
    password = PasswordField('Password:', validators=[DataRequired()])    # field required , type password
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):  # create Register class
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

    def validate_username(self, username):              # username not already exit
        user = User.query.filter_by(username=username.data).first()
        if user is not None: # username exit in db
            raise ValidationError('Please use a different Username')

    def validate_email(self, email):                             # email not already exit
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different Email')


class EditProfileForm(FlaskForm):     # create Edit Profile edit form
    username = StringField("New Username", validators=[DataRequired()])
    email = StringField("New Email", validators=[Email()])
    about_me = TextAreaField("About_me", validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class PostForm(FlaskForm):
    post = TextAreaField('Say something:', validators=[DataRequired(), Length(min=1, max= 140)])
    submit = SubmitField('Send')


class ResetPasswordFormRequest(FlaskForm):   # form of Reset Password
    email = StringField('Email:', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password Request')


class ResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Reset Password")
