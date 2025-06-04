from flask import Blueprint, render_template, redirect, url_for, flash, session
import sqlite3

home_bp = Blueprint('home', __name__)

@home_bp.route('/home', methods=['GET'])
def home():
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    username = session.get('username', 'ゲスト')

    # travel_data をデータベースから取得
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row  # dict型でアクセス可能にする
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM travel_data
    """)
    travel_data_list = cursor.fetchall()

    conn.close()

    return render_template('home.html', user_id=user_id, username=username, travel_data_list=travel_data_list)
