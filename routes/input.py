from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import check_password_hash

input_bp = Blueprint('input', __name__)

@input_bp.route('/input', methods=['GET'])
def input():
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))
    user_id = session['user_id']
    username = session.get('username', 'ゲスト')
    return render_template('input.html', username=username)