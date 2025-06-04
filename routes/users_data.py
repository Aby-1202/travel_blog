from flask import Blueprint, render_template, redirect, url_for, flash, session
import sqlite3

users_data_bp = Blueprint('users_data', __name__)

@users_data_bp.route('/users_data', methods=['GET'])
def users_data():
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    username = session.get('username', 'ゲスト')


    return render_template('users_data.html', user_id=user_id, username=username)
