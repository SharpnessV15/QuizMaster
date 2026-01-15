from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, RadioField, TextAreaField, TimeField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError,Regexp
from datetime import time
import models



class loginForm(FlaskForm):
    email = StringField(label='Username:', validators=[ DataRequired()])
    password = PasswordField(label='Password: ', validators=[Length(min=8, max=70), DataRequired()])
    submit=SubmitField(label='Submit')

class registerForm(FlaskForm):
    def validate_email(self,email_to_check):
        email=models.User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email already exists. Please choose a different one.')
        
    firstname=StringField(label = 'First Name:', validators=[Length(min=2, max=30), DataRequired()])
    lastname=StringField(label = 'Last Name:' ,validators=[Length(min=2, max=30), DataRequired()])
    qualification=StringField(label='Qualifications:', validators=[Length(min=2, max=300), DataRequired()])
    dob=DateField(label='Date of birth:', validators=[DataRequired()])
    email = StringField(label='Username(email):', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=8, max=70), DataRequired()])
    checkpwd= PasswordField(label='Enter password again:', validators=[EqualTo('password'), DataRequired()])
    submit= SubmitField(label='Submit')

class createSubForm(FlaskForm):
    def validate_subname(self,subject_to_check):
        existing_subject = models.Subject.query.filter_by(name=subject_to_check.data).first()
        if existing_subject and existing_subject.id != self.subject_id:
            raise ValidationError('Subject already exists. Please choose a different one.')
    subname=StringField(label='Subject Name:', validators=[Length(min=2, max=16), DataRequired()])
    subdesc=TextAreaField(label='Description:', validators=[Length(min=2, max=500), DataRequired()])
    submit=SubmitField(label='Submit')

class createChpForm(FlaskForm):
    def validate_chpname(self,chp_to_check):
        existing_chapter = models.Chapter.query.filter_by(name=chp_to_check.data).first()
        if existing_chapter and existing_chapter.id != self.chapter_id:
            raise ValidationError('Chapter already exists. Please choose a different one.')
    chpname=StringField(label='Chapter Name:', validators=[Length(min=2, max=16), DataRequired()])
    chpdesc=TextAreaField(label='Description:', validators=[Length(min=2, max=500), DataRequired()])
    submit=SubmitField(label='Submit')

class createQuizForm(FlaskForm):
    def validate_quizname(self,quiz_to_check):
        name=models.Quiz.query.filter_by(name=quiz_to_check.data).first()
        if name:
            raise ValidationError('Quiz already exists. Please create a new one.')
    
    quizname = StringField(label='Quiz Name:', validators=[Length(min=2, max=16), DataRequired()])
    date = DateField(label='Date of Quiz:', validators=[DataRequired()])
    time_duration = StringField(label='Time Duration (HH:MM):', validators=[DataRequired(),Regexp('^([0-9]{2}):([0-9]{2})$', message='Invalid time format. Use HH:MM.')])
    remarks = TextAreaField(label='Remarks:', validators=[Length(min=2, max=500), DataRequired()])
    submit = SubmitField(label='Submit')

class createQuesForm(FlaskForm):
    question_statement=StringField(label='Question:', validators=[Length(min=2, max=500), DataRequired()])
    correct_option=RadioField('Correct Option', choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')], validators=[DataRequired()])
    option1=StringField(label='Option 1:', validators=[Length(min=2, max=10), DataRequired()])
    option2=StringField(label='Option 2:', validators=[Length(min=2, max=10), DataRequired()])
    option3=StringField(label='Option 3:', validators=[Length(min=2, max=10), DataRequired()])
    option4=StringField(label='Option 4:', validators=[Length(min=2, max=10), DataRequired()])
    submit=SubmitField(label='Submit')
