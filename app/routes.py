from sqlalchemy.sql.functions import user
from app import App                      # import the App instance from app folder
from app import db                       
from app.models import User, Post        
from app.email import send_password_email, send_email
from flask import render_template        
from app.forms import LoginForm          
from app.forms import RegisterForm       
from app.forms import EditProfileForm   
from app.forms import PostForm           
from app.forms import ResetPasswordFormRequest  
from app.forms import ResetForm         
from app.forms import EmailForm
from flask import flash                 # import flash: to shows msg to user ( print )
from flask import redirect              # to navigate to another URL
from flask import get_flashed_messages
from flask_login import current_user    
from flask_login import login_user     
from flask_login import login_required 
# contains all the information that the client sent
from flask import request              
from werkzeug.urls import url_parse    
from flask_login import logout_user     # import logout_user
from flask import url_for               # to generates URLs
from datetime import datetime           # import datetime
from app.camera import VideoCamera
from flask import Response
user_fake = {'username': 'Mohamed'}          # create a fake user
posts_fake = [                               # create a fake posts : list of dict
              {
                'author': {'username': 'Alex'},
                'body': 'This is a good day'
              },
              {
                'author': {'username': 'Myriam'},
                'body': 'Wow you are amazing!'
              },
              {
                  'author': {'username': 'Ahmed'},
                  'body': 'Can I plat this game'
              }
        ]
attempts = 0 


@login_required
@App.route('/camera')
def camera():
    return render_template("camera.html", title="Camera")


def gen(camera):
    while True:
        frame = camera.get_stream()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@App.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@App.route("/", methods=['GET', 'POST'])                # decorator, App : instance
@App.route("/index", methods=['GET', 'POST'])           # decorator : modifies the function that flow it
@login_required                                         # to protect a view function from not authenticated users
def index():

    form_post = PostForm()
    if form_post.validate_on_submit():
        new_post = Post(body=form_post.post.data, user=current_user)
        db.session.add(new_post)
        db.session.commit()
       # flash("Your post is new live!")
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)

    all_posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, App.config['POSTS_PER_PAGE'], False)

    next_url = url_for('index', page=all_posts.next_num) if all_posts.has_next else None  # check for next page
    prev_url = url_for('index', page=all_posts.prev_num) if all_posts.has_prev else None  # ckeck for previous page

    return render_template("index.html", title="Home Page", form=form_post, posts=all_posts.items, next_url=next_url,
                           prev_url=prev_url)    # the response
    # we send user dict

    # url_for() : name of the view function the some with mapURL





@App.route("/login", methods=['GET', 'POST'])    # this view function accepts GET , POST methods
def login():
    user_ = None
    global attempts
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form_ = LoginForm()                                         # create the loginForm object

    if form_.validate_on_submit():                              # when validate the from
        user_ = User.query.filter_by(username=form_.username.data).first()
        user_email= User.query.filter_by(email=form_.username.data).first()

        if attempts >= int(App.config['MAX_ATTEMPTS']):
            # print("attempts: ", attempts)
            return render_template("locked.html", title="locked")

        if user_ is None or not user_.check_password(form_.password.data):  # no user input  or wrong password
            flash('Invalid username or password')
            attempts += 1
            # print("attempts : ", attempts)
            return redirect(url_for('login'))

            # form_.remember_me.data, form_.username.errors))    # .data : what the user has entered
        login_user(user_, remember=form_.remember_me.data)
        next_page = request.args.get('next')                     # request.args -> dict format
        if not next_page or url_parse(next_page).netloc != '':
            attempts = 0
            next_page = url_for('index')
        return redirect(next_page)

    return render_template("Login.html", title="Log in", form=form_)


@App.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))   # return the index page


@App.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:   # make sure that the user is not logged
        return redirect(url_for('index'))
    form_reg = RegisterForm()
    if form_reg.validate_on_submit():

        user_reg = User(username=form_reg.username.data, email=form_reg.email.data)
        user_reg.set_password(form_reg.password.data)
        db.session.add(user_reg)
        db.session.commit()
        flash('Congratulation, You are now a registered user !')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form_reg)


@App.route('/user/<username>')
@login_required       # only for logged in users
def user(username):
    user_porfile = User.query.filter_by(username=username).first_or_404()  # the first ( = exist 'username' ) or
    # 404 to the client

    PATH= "/user/" + str(user_porfile.username) + "/sendEmail"

    posts = [
        {'author': user_porfile, 'body': 'Test post #1'},
        {'author': user_porfile, 'body': 'Test post #2'}
    ]
    page = request.args.get('page', 1, type=int)

    my_posts = user_porfile.posts.order_by(Post.timestamp.desc()).paginate(page, App.config['POSTS_PER_PAGE'],False)

    # check for next page
    next_url = url_for('user', username=user_porfile.username, page=my_posts.next_num) if my_posts.has_next else None
    # ckeck for previous page
    prev_url = url_for('user', username=user_porfile.username, page=my_posts.prev_num) if my_posts.has_prev else None
    return render_template('user.html', title="profile", user=user_porfile, posts=my_posts.items, next_url=next_url,
                           prev_url=prev_url, PATH=PATH)


@App.route('/user/<username>/sendEmail', methods=['GET', 'POST'])
@login_required
def sendEmail(username):
    # user_profile ( receiver  user_profile.email)
    # current_user ( sender : current_user.email)
    user_porfile = User.query.filter_by(username=username).first_or_404()  # the first ( = exist 'username' ) or
    email_form = EmailForm()
    print(user_porfile.email)
    print('current user', current_user.email)
    if email_form.validate_on_submit():
        subject = email_form.subject.data
        body = email_form.mail.data
        send_email(str(subject), sender=current_user.email, recipients=[user_porfile.email],
                   text_body='',
                   html_body=body + '''<br><h2> To reply go to <a href="https://ahmed-nouira-blog4.herokuapp.com"> The BLOG ^^ </a></h2>
                   ''')

        flash('Your Have send an Email to {}'.format(user_porfile.username))
        return redirect(url_for('sendEmail', username=user_porfile.username))
    return render_template('send_email.html', title="sendEmail", form=email_form)


@App.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():  # !!!!!!!!!

    #if current_user.is_authenticated:   # make sure that the user is not logged
     #   return redirect(url_for('edit_profile'))

    form_edit = EditProfileForm(current_user.username)
    if form_edit.validate_on_submit():
        current_user.username = form_edit.username.data
        current_user.about_me = form_edit.about_me.data
        new_user = User(username=form_edit.username.data, about_me=form_edit.username.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':

        form_edit.username.data = current_user.username
        form_edit.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form_edit)


@App.route("/reset_password_request", methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:  # making sure the user is not logged in( have right password and email )
        return redirect(url_for('index'))
    form_rest = ResetPasswordFormRequest()
    if form_rest.validate_on_submit():
        user_rest = User.query.filter_by(email=form_rest.email.data).first()
        if user_rest:
            send_password_email(user_rest)
            flash('Check your email to reset your password')
            return redirect(url_for('login'))
        else:
            flash('This email is not registered!!!!')
            return redirect(url_for('reset_password_request'))
    return render_template("reset_password_request.html", title="Reset_Request", form=form_rest)


@App.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user_re_psw = User.verify_reset_password(token)
    if not user_re_psw:
        return redirect(url_for('index'))
    form_re_psw = ResetForm()
    if form_re_psw.validate_on_submit():
        user_re_psw.set_password(form_re_psw.password.data)
        db.session.commit()
        flash('Your password have been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title="Reset", form=form_re_psw)


@App.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
