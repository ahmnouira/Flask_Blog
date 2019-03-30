from flask_mail import Message           # import Message
from app import App, mail                # import App, mail
from flask import render_template        # import render_template
from threading import Thread             # import Thread to send the emails in background


def send_email(subject, sender, recipients, text_body, html_body):  # helper function from emails
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_sync_email, args=(App, msg)).start()


def send_sync_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_password_email(user):
    token = user.get_reset_password_token()
    send_email('[Blog] Reset Your Password', sender=App.config['ADMINS'][0], recipients=[user.email],
               text_body=render_template('email_/reset_password.txt', user=user, token=token),
               html_body=render_template('email_/reset_password.html', user=user, token=token))
