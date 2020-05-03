from data import db_session
from main import app, for_admins
from flask import render_template


@app.route('/test')
@for_admins
def test():
    return render_template('main.html', title='Главная')
