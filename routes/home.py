from flask import Blueprint, render_template, redirect, url_for, flash, session
import sqlite3
from datetime import datetime

home_bp = Blueprint('home', __name__)

@home_bp.route('/home', methods=['GET'])
def home():
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    username = session.get('username', 'ゲスト')

    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT travel_data.*, users_table.u_name AS username
        FROM travel_data
        JOIN users_table ON travel_data.u_id = users_table.id
    """)
    travel_data_list = cursor.fetchall()

    conn.close()

    # 日数計算を追加
    travel_data_with_duration = []
    for travel in travel_data_list:
        try:
            start_date = datetime.strptime(travel['start_date'], "%Y-%m-%d")
            end_date = datetime.strptime(travel['end_date'], "%Y-%m-%d")
            duration_days = (end_date - start_date).days + 1  # 1日も含めるため+1
        except Exception:
            duration_days = "不明"

        # sqlite3.Row は辞書風だけどイミュータブルなので辞書に変換して加工
        travel_dict = dict(travel)
        travel_dict['duration_days'] = duration_days
        travel_data_with_duration.append(travel_dict)

    return render_template(
        'home.html',
        user_id=user_id,
        username=username,
        travel_data_list=travel_data_with_duration
    )
