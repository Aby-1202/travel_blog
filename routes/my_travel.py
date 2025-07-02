from flask import Blueprint, render_template, redirect, url_for, flash, session
import sqlite3
from datetime import datetime

my_travel_bp = Blueprint('my_travel', __name__)

@my_travel_bp.route('/my_travel', methods=['GET'])
def my_travel():
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    username = session.get('username', 'ゲスト')

    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            td.*,
            ut.u_name        AS username,
            -- 累計ブックマーク数
            (SELECT COUNT(*) FROM bookmark_data WHERE t_id = td.id) AS bookmark_count,
            -- 累計いいね数
            (SELECT COUNT(*) FROM favorites     WHERE t_id = td.id) AS favorite_count
        FROM travel_data td
        JOIN users_table ut
            ON td.u_id = ut.id
        WHERE td.u_id = ?
        ORDER BY td.start_date DESC
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
        'my_travel.html',
        user_id=user_id,
        username=username,
        travel_data_list=travel_data_with_duration
    )
