from flask import Blueprint, render_template, redirect, url_for, flash, session
import sqlite3
from datetime import datetime

bookmark_bp = Blueprint('bookmark', __name__)

@bookmark_bp.route('/bookmark', methods=['GET'])
def bookmark():
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    username = session.get('username', 'ゲスト')

    conn = sqlite3.connect('travel_blog/app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT travel_data.*, users_table.u_name AS username, bookmark_data.id AS bookmark_id
        FROM travel_data
        JOIN bookmark_data ON travel_data.id = bookmark_data.id
        WHERE bookmark_data.u_id = ?
        ORDER BY bookmark_data.b_created_at DESC
    """, (user_id,))
    travel_data_list = cursor.fetchall()
    conn.close()

    travel_data_with_duration = []
    for travel in travel_data_list:
        try:
            start_date = datetime.strptime(travel['start_date'], "%Y-%m-%d")
            end_date = datetime.strptime(travel['end_date'], "%Y-%m-%d")
            duration_days = (end_date - start_date).days + 1
        except Exception:
            duration_days = "不明"

        travel_dict = dict(travel)
        travel_dict['duration_days'] = duration_days
        travel_data_with_duration.append(travel_dict)

    return render_template(
        'home.html',
        user_id=user_id,
        username=username,
        travel_data_list=travel_data_with_duration
    )
