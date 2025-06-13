import os
from flask import Blueprint, render_template, redirect, url_for, flash, session, request, current_app
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

    # データベースに接続
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT travel_data.*, users_table.u_name AS username, bookmark_data.id AS bookmark_id
        FROM travel_data
        JOIN bookmark_data ON travel_data.id = bookmark_data.t_id
        JOIN users_table ON travel_data.u_id = users_table.id
        WHERE bookmark_data.u_id = ?
        ORDER BY bookmark_data.b_created_at DESC
    """, (user_id,))
    
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

@bookmark_bp.route('/bookmark/save', methods=['POST'])
def save_bookmark():
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    travel_id = request.form.get('travel_id')  # フロントから送信された旅行データの ID

    if travel_id:
        # データベースに接続
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # ブックマークをデータベースに追加
        cursor.execute("""
            INSERT INTO bookmark_data (u_id, t_id, b_created_at)
            VALUES (?, ?, ?)
        """, (user_id, travel_id, datetime.now()))

        conn.commit()
        conn.close()

        flash('ブックマークを保存しました。', 'success')
    else:
        flash('ブックマークの保存に失敗しました。', 'danger')

    return redirect(url_for('home.home'))  # ホームにリダイレクト