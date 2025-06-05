from flask import Blueprint, render_template, redirect, url_for, flash, session
import sqlite3

users_data_bp = Blueprint('users_data', __name__)

@users_data_bp.route('/users_data', methods=['GET'])
def users_data():
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    user_id = session['user_id']

    # DB接続
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # ユーザー情報を取得
    cursor.execute("""
        SELECT id, u_name, email, password
        FROM users_table
        WHERE id = ?
    """, (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        flash("ユーザー情報が見つかりません。")
        return redirect(url_for('home.home'))

    return render_template('users_data.html',
                           user_id=user['id'],
                           username=user['u_name'],
                           email=user['email'],
                           password=user['password'])
