from flask import render_template,redirect,url_for,request,flash
from config import app,db
from forms import registerForm,loginForm,createSubForm,createChpForm,createQuizForm,createQuesForm
from models import User,Subject,Chapter,Quiz,Questions,Scores
from flask_login import login_user, logout_user, login_required,current_user
from datetime import datetime,time

@app.route('/')
def start():
    return render_template("startPage.html")
@app.route('/sub')
@login_required
def index():
    subject = Subject.query.all()
    chapters = Chapter.query.all()
    return render_template("home.html",subject=subject,chapters=chapters)


@app.route('/register', methods=['POST','GET'])
def register():
    form=registerForm()
    if form.validate_on_submit() and not User.query.filter_by(email=form.email.data).first():
        newUser= User(name=form.firstname.data+" "+form.lastname.data,email=form.email.data,password=form.password.data,qualification=form.qualification.data,dob=form.dob.data)
        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for('login'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg[0]}', category='danger') 
    return render_template("register.html",form=form)


@app.route('/login', methods=['POST','GET'])
def login():
    form=loginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and user.password==form.password.data:
            login_user(user)
            flash(f'Welcome back {user.name}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category='danger')    
    return render_template("login.html", form=form)

@app.route('/logout', methods=['POST','GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/CreateSub', methods=['POST','GET'])
@login_required
def subcre():
    form=createSubForm()
    if form.validate_on_submit():
        newSub=Subject(name=form.subname.data,description=form.subdesc.data)
        db.session.add(newSub)
        db.session.commit()
        return redirect(url_for('index'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg[0]}', category='danger')
    if current_user.email=="admin":
        return render_template("subcre.html",form=form)
    else:
        return redirect(url_for('index'))
    
@app.route('/deleteSub/<int:id>', methods=['POST','GET'])
@login_required
def subdel(id):
    if current_user.email=="admin":
        delsub=Subject.query.filter_by(id=id).first()
        db.session.delete(delsub)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    
@app.route('/subject/<sid>', methods=['POST','GET'])
@login_required
def chapters(sid): 
    subject=Subject.query.filter_by(id=sid).first()
    chapters=Chapter.query.filter_by(subject_id=sid).all()
    quizzes = Quiz.query.filter(Quiz.chapter_id.in_([chapter.id for chapter in chapters])).all()
    return render_template("chapters.html",subject=subject,chapters=chapters,quizzes=quizzes)

@app.route('/CreateChp/<sid>', methods=['POST','GET'])
@login_required
def chpcre(sid):
    form=createChpForm()
    if form.validate_on_submit():
        newChp=Chapter(name=form.chpname.data,description=form.chpdesc.data,subject_id=sid)
        db.session.add(newChp)
        db.session.commit()
        return redirect(url_for('chapters',sid=sid))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg[0]}', category='danger')
    if current_user.email=="admin":
        return render_template("chpcre.html",form=form,sid=sid)
    else:
        return redirect(url_for('chapters',sid=sid))
    
@app.route('/deleteChp/<int:cid>', methods=['POST','GET'])
@login_required
def chpdel(cid):
    if current_user.email=="admin":
        delchp=Chapter.query.filter_by(id=cid).first()
        sid=delchp.subject_id
        db.session.delete(delchp)
        db.session.commit()
        return redirect(url_for('chapters', sid=sid))
    else:
        return redirect(url_for('index'))
    
@app.route('/chapter/<cid>', methods=['POST','GET'])
@login_required
def quizzes(cid):
    chapter=Chapter.query.filter_by(id=cid).first() 
    quizzes=Quiz.query.filter_by(chapter_id=cid).all()
    if quizzes != []:
        scores=Scores.query.filter_by(user_id=current_user.id).all()
        return render_template("quizzes.html",chapter=chapter,quizzes=quizzes,scores=scores)
    else:
        return render_template("quizzes.html",chapter=chapter,quizzes=quizzes)

@app.route('/CreateQuiz/<cid>', methods=['POST','GET'])
@login_required
def quizcre(cid):
    form=createQuizForm()
    if current_user.email=="admin":
        if form.validate_on_submit():
            hours,minutes=form.time_duration.data.split(':')
            timed=time(hour=int(hours),minute=int(minutes))
            newQuiz=Quiz(name=form.quizname.data,date_of_quiz=form.date.data,time_duration=timed,remarks=form.remarks.data,chapter_id=cid)
            db.session.add(newQuiz)
            db.session.commit()
            return redirect(url_for('questioncre',qid=newQuiz.id))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'{err_msg[0]}', category='danger')
        return render_template("quizcre.html",form=form,cid=cid)
    return redirect(url_for('quizzes', cid=cid))

@app.route('/AddQuestion/<qid>', methods=['POST','GET'])
@login_required
def questioncre(qid):
    cid=Quiz.query.filter_by(id=qid).first().chapter_id
    if current_user.email=="admin":
        form=createQuesForm()
        form.qid=qid
        questions=Questions.query.filter_by(quiz_id=qid).all()
        if form.validate_on_submit():
            form.correct_option.data=int(form.correct_option.data)
            newQues=Questions(quiz_id=qid,question_statement=form.question_statement.data,correct_option=form.correct_option.data,option1=form.option1.data,option2=form.option2.data,option3=form.option3.data,option4=form.option4.data)
            db.session.add(newQues)
            db.session.commit()
            return redirect(url_for('questioncre',qid=qid)) 
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'{err_msg[0]}', category='danger')   
        return render_template("questioncre.html",form=form,questions=questions,cid=cid)
    return redirect(url_for('quizzes', cid=cid))

@app.route('/delete/<int:qid>', methods=['POST','GET'])
@login_required
def quizdel(qid):
    if current_user.email=="admin":
        delquiz=Quiz.query.filter_by(id=qid).first()
        cid=delquiz.chapter_id
        db.session.delete(delquiz)
        db.session.commit()
        return redirect(url_for('quizzes', cid=cid))
    else:
        return redirect(url_for('quizzes', cid=cid))

@app.route('/delete/ques/<int:quesid>', methods=['POST','GET'])
@login_required
def quesdel(quesid):
    if current_user.email=="admin":    
        delques=Questions.query.filter_by(id=quesid).first()
        qid=delques.quiz_id
        db.session.delete(delques)
        db.session.commit()
        if Questions.query.filter_by(quiz_id=qid).all() == []:
            delquiz=Quiz.query.filter_by(id=qid).first()
            db.session.delete(delquiz)
            db.session.commit()
            return redirect(url_for('quizzes', cid=delquiz.chapter_id))
        return redirect(url_for('questioncre', qid=qid))
    else:
        return redirect(url_for('questioncre', qid=qid))
    
@app.route('/QuizCheck/<int:qid>', methods=['POST','GET'])
@login_required
def quizcheck(qid):
    quiz = Quiz.query.filter_by(id=qid).first()
    questions = Questions.query.filter_by(quiz_id=qid).all()
    score=0
    total_questions=len(questions)
    if request.method=='POST':
        for question in questions:
            answer = request.form.get(str(question.id))
            if answer:
                if int(answer) == question.correct_option :
                    score=score+1
        percent=(float(score)/float(total_questions))*100 if total_questions > 0 else 0
        if not Scores.query.filter_by(quiz_id=qid, user_id=current_user.id).first():
            newScore = Scores(quiz_id=qid, user_id=current_user.id, time_stamp_of_attempt=datetime.now(), total_scored=score, percentage=percent)
            db.session.add(newScore)
            db.session.commit()
        else:
            oldScore = Scores.query.filter_by(quiz_id=qid, user_id=current_user.id).first()
            oldScore.total_scored = score
            oldScore.percentage = percent
            db.session.commit()
        return redirect(url_for('scores'))
    return redirect(url_for('index'))
    
@app.route('/quiz/<int:qid>', methods=['POST','GET'])
@login_required
def quiz(qid):
    if current_user.email != "admin":
        questions = Questions.query.filter_by(quiz_id=qid).all()
        return render_template("theQuiz.html",questions=questions)
    return redirect(url_for('quizzes', cid=Quiz.query.filter_by(id=qid).first().chapter_id))

@app.route('/score/<int:uid>', methods=['POST','GET'])
@app.route('/scores', methods=['POST','GET'])
@login_required
def scores(uid=None):
    
    subjects=Subject.query.all()
    chapters=Chapter.query.all()
    chartData = {}
    if current_user.email != "admin":
        quizzes = []
        scores = Scores.query.filter_by(user_id=current_user.id).order_by(Scores.time_stamp_of_attempt).all()
        for score in scores:
            quiz = Quiz.query.filter_by(id=score.quiz_id).first()
            quizzes.append(Quiz.query.filter_by(id=score.quiz_id).first())

            if quiz.chapter_id not in chartData:
                chartData[quiz.chapter_id] = {
                    'labels':[],
                    'scores':[]
                }

            chartData[quiz.chapter_id]['labels'].append(quiz.name)
            chartData[quiz.chapter_id]['scores'].append(score.percentage)



        return render_template("scores1.html",subjects=subjects, chapters=chapters, quizzes=quizzes,scores=scores, uid=current_user.id, chartData=chartData)
    else:
        quizzes = []
        scores = Scores.query.filter_by(user_id=uid).order_by(Scores.time_stamp_of_attempt).all()
        for score in scores:
            quizzes.append(Quiz.query.filter_by(id=score.quiz_id).first())
        return render_template("scores1.html",subjects=subjects, chapters=chapters, quizzes=quizzes,scores=scores, uid=uid, chartData=chartData)
    
@app.route('/search', methods=['POST','GET'])
@login_required
def search():
    search_query = request.args.get('query')
    if search_query:
        subjects = Subject.query.filter(Subject.name.like('%' + search_query + '%')).all()
        chapters = Chapter.query.filter(Chapter.name.like('%' + search_query + '%')).all()
        quizzes = Quiz.query.filter(Quiz.name.like('%' + search_query + '%')).all()
        users= User.query.filter(User.name.like('%' + search_query + '%')).all()
        return render_template("search.html", subjects=subjects, chapters=chapters, quizzes=quizzes, users=users)
    else:
        return redirect(url_for('index'))
    
@app.route('/admScores', methods=['POST','GET'])
@login_required
def admScores():
    if current_user.email=="admin":
        users = User.query.all()
        return render_template("admScores.html", users=users)
    else:
        return redirect(url_for('index'))
    
@app.route('/editch/<int:cid>', methods=['POST','GET'])
@login_required
def editc(cid):
    if current_user.email=="admin":
        chapter = Chapter.query.filter_by(id=cid).first()
        form = createChpForm()
        form.chapter_id = chapter.id
        if form.validate_on_submit():
            chapter.name = form.chpname.data
            chapter.description = form.chpdesc.data
            db.session.commit()
            return redirect(url_for('chapters', sid=chapter.subject_id))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'{err_msg[0]}', category='danger')
        form.chpname.data = chapter.name
        form.chpdesc.data = chapter.description
        return render_template("editch.html", form=form, chapter=chapter, sid=chapter.subject_id)
    else:
        return redirect(url_for('index'))
    
@app.route('/edits/<int:sid>', methods=['POST','GET'])
@login_required
def edits(sid):
    if current_user.email=="admin":
        subject = Subject.query.filter_by(id=sid).first()
        form = createSubForm()
        form.subject_id = subject.id
        if form.validate_on_submit():
            subject.name = form.subname.data
            subject.description = form.subdesc.data
            db.session.commit()
            return redirect(url_for('index'))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'{err_msg[0]}', category='danger')
        form.subname.data = subject.name
        form.subdesc.data = subject.description
        return render_template("edits.html", form=form, subject=subject)
    else:
        return redirect(url_for('index'))