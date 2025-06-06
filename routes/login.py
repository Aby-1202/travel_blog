from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import check_password_hash

login_bp = Blueprint('login', __name__)

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('travel_blog/app.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id, u_name, password_hash FROM users_table WHERE u_name = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]       # id を保存
            session['username'] = user[1]      # u_name を保存
            flash("ログインに成功しました")
            return redirect(url_for('home.home'))
        else:
            flash("ユーザ名またはパスワードが間違っています")
            return render_template('login.html')

    return render_template('login.html')
