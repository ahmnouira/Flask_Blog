from flask import Flask                          # import flask lib
from app.config import Config                    # import Class Config from file config which is inside app folder
from flask_sqlalchemy import SQLAlchemy          # import SQLAlchemy
from flask_login import LoginManager             # to manage the user logged in state
from flask_migrate import Migrate                # import Migrate
from flask_mail import Mail                      # import Mail
from flask_bootstrap import Bootstrap            # import Bootstrap extension
import logging
import os
from logging.handlers import SMTPHandler          # import SMTPHandler
from logging.handlers import RotatingFileHandler  # import RotatingFileHandler
App = Flask(__name__)                             # create the App instance
App.config.from_object(Config)                    # tell flask to read it and apply Config
db = SQLAlchemy(App)                              # create the database of the app
migrate = Migrate(App, db)                        # create the migration engine
login = LoginManager(App)                         # create the login object
mail = Mail(App)                                  # create mail instance
bootstrap = Bootstrap(App)
login.login_view = 'login'                        # what is the view function that handles logins

from app import routes, models, errors            # import routes, models, errors from app folder

if not App.debug:   # get errors in the production mode

    # get error with emails
    if App.config['MAIL_SERVER']:
        auth = None
        if App.config['MAIL_USERNAME'] or App.config['MAIL_PASSWORD']:
            auth = (App.config['MAIL_USERNAME'], App.config['MAIL_PASSWORD'])
        secure = None
        if App.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(App.config['MAIL_SERVER'], App.config['MAIL_PORT']),
            fromaddr='no-rely@' + App.config['MAIL_SERVER'],
            toaddrs=App.config['ADMINS'], subject='Blog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        App.logger.addHandler(mail_handler)

    if App.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        App.logger.addHandler(stream_handler)

    else:
        # writing the log File
        if not os.path.exists('logs'):
            os.mkdir('logs')   # create logs if not exists
        # create blog.log file and sets the log file size to 10KB and keep the last ten log files as backup
        # RotatingFileHandler ensure that the log files do not grow too large when the app runs for a long time
        file_handler = RotatingFileHandler('logs/blog.log', maxBytes=1024, backupCount=10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        App.logger.addHandler(file_handler)
    App.logger.setLevel(logging.INFO)
    App.logger.info('Blog Startup')




