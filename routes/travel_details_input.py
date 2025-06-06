import traceback
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from datetime import datetime

travel_details_input_bp = Blueprint('travel_details_input', __name__, url_prefix='')


@travel_details_input_bp.route('/travel/<int:travel_id>/details')
def travel_details(travel_id):
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT travel_data.*, users_table.u_name AS username
        FROM travel_data
        JOIN users_table ON travel_data.u_id = users_table.id
        WHERE travel_data.id = ?
    """, (travel_id,))
    travel = cursor.fetchone()
    conn.close()

    if not travel:
        flash("指定された旅行は存在しません。")
        return redirect(url_for('my_travel.my_travel'))

    # 日数計算
    try:
        start_date = datetime.strptime(travel['start_date'], "%Y-%m-%d")
        end_date = datetime.strptime(travel['end_date'], "%Y-%m-%d")
        duration_days = (end_date - start_date).days + 1
    except Exception:
        duration_days = "不明"

    travel_dict = dict(travel)
    travel_dict['duration_days'] = duration_days

    return render_template(
        'travel_details_input.html',
        travel=travel_dict
    )
