from flask import render_template
from app import App, db


@App.errorhandler(404)
def not_found_page(error):
    return render_template('404.html', title="Not Found Page"), 404


@App.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', title="Internal Error"), 500

