import traceback
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from datetime import datetime

travel_details_input_bp = Blueprint('travel_details_input', __name__, url_prefix='')


@travel_details_input_bp.route('/travel/<int:travel_id>/details')
def travel_details(travel_id):
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    username = session.get('username', 'ゲスト')

    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 旅行情報を取得
    cursor.execute("""
        SELECT travel_data.*, users_table.u_name AS username
        FROM travel_data
        JOIN users_table ON travel_data.u_id = users_table.id
        WHERE travel_data.id = ?
    """, (travel_id,))
    travel = cursor.fetchone()

    if not travel:
        conn.close()
        flash("指定された旅行は存在しません。")
        return redirect(url_for('my_travel.my_travel'))

    # POST時は詳細追加処理
    if request.method == 'POST':
        day_number = request.form.get('day_number')
        detail_name = request.form.get('detail_name')
        detail_text = request.form.get('detail_text')
        visit_time = request.form.get('visit_time')
        location_url = request.form.get('location_url')

        if not (day_number and detail_name):
            flash("日数と詳細タイトルは必須です。")
        else:
            try:
                cursor.execute("""
                    INSERT INTO travel_details (travel_data_id, detail_name, detail_text, day_number, visit_time, location_url)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (travel_id, detail_name, detail_text, int(day_number), visit_time, location_url))
                conn.commit()
                flash("旅行詳細を追加しました。")
                return redirect(url_for('travel_details_input.travel_details', travel_id=travel_id))
            except Exception as e:
                flash(f"追加に失敗しました: {e}")

    # 旅行詳細一覧を取得
    cursor.execute("""
        SELECT * FROM travel_details
        WHERE travel_data_id = ?
        ORDER BY day_number, visit_time
    """, (travel_id,))
    travel_details = cursor.fetchall()

    conn.close()

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
        travel=travel_dict,
        travel_details=travel_details,
        username=username
    )


@travel_details_input_bp.route('/travel/<int:travel_id>/details/add', methods=['POST'])
def add_travel_detail(travel_id):
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    detail_name = request.form.get('detail_name')
    detail_text = request.form.get('detail_text')
    day_number = request.form.get('day_number')
    visit_time = request.form.get('visit_time')
    location_url = request.form.get('location_url')

    # 入力チェックなど必要に応じて

    conn = sqlite3.connect('travel_blog/app.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO travel_details (travel_data_id, detail_name, detail_text, day_number, visit_time, location_url)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (travel_id, detail_name, detail_text, day_number, visit_time, location_url))
    conn.commit()
    conn.close()

    flash("旅行詳細を追加しました。")
    return redirect(url_for('travel_details_input.travel_details', travel_id=travel_id))
