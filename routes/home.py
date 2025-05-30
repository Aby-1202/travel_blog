from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import check_password_hash

home_bp = Blueprint('home', __name__)

@home_bp.route('/home', methods=['GET'])
def home():
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))
    user_id = session['user_id']
    username = session.get('username', 'ゲスト')
    return render_template('home.html', username=username)