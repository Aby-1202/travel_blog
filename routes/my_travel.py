from flask import Blueprint, render_template, redirect, url_for, flash, session
import sqlite3

my_travel_bp = Blueprint('my_travel', __name__)

@my_travel_bp.route('/my_travel', methods=['GET'])
def my_travel():
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    username = session.get('username', 'ゲスト')


    return render_template('my_travel.html', user_id=user_id, username=username)
