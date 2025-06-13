import traceback
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from werkzeug.utils import secure_filename

edit_bp = Blueprint('edit', __name__)

@edit_bp.route('/edit/<int:travel_id>', methods=['GET', 'POST'])
def edit(travel_id):
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    username = session.get('username', 'ゲスト')

    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == 'POST':
        try:
            # 旅行基本情報
            title = request.form['title']
            location = request.form['location']
            human_number = request.form['human_number']
            overview = request.form['overview']
            start_date = request.form['start_date']
            end_date = request.form['end_days']

            # 画像
            photo = request.files.get('photo')
            image_path = None
            if photo and photo.filename:
                filename = secure_filename(photo.filename)
                image_path = os.path.join('static/images', filename)
                photo.save(image_path)

            # 旅行基本情報を更新
            update_sql = """
                UPDATE travel_data
                SET t_title = ?, t_location = ?, human_number = ?, overview = ?, start_date = ?, end_date = ?
                WHERE id = ? AND u_id = ?
            """
            cursor.execute(update_sql, (title, location, human_number, overview, start_date, end_date, travel_id, user_id))

            if image_path:
                cursor.execute("UPDATE travel_data SET image_path = ? WHERE id = ?", (image_path, travel_id))

            # --------------------
            # travel_details の処理
            # --------------------
            # 既存データの更新
            detail_ids = request.form.getlist('detail_id')
            for detail_id in detail_ids:
                dname = request.form.get(f'detail_name_{detail_id}')
                dtext = request.form.get(f'detail_text_{detail_id}')
                dday = request.form.get(f'day_number_{detail_id}')
                dtime = request.form.get(f'visit_time_{detail_id}')
                durl = request.form.get(f'location_url_{detail_id}')

                cursor.execute("""
                    UPDATE travel_details
                    SET detail_name = ?, detail_text = ?, day_number = ?, visit_time = ?, location_url = ?
                    WHERE id = ? AND travel_data_id = ?
                """, (dname, dtext, dday, dtime, durl, detail_id, travel_id))

            # 削除対象の詳細情報
            delete_ids = request.form.getlist('delete_detail')
            for delete_id in delete_ids:
                cursor.execute("DELETE FROM travel_details WHERE id = ? AND travel_data_id = ?", (delete_id, travel_id))

            # 新規追加データ
            new_names = request.form.getlist('new_detail_name')
            new_texts = request.form.getlist('new_detail_text')
            new_days = request.form.getlist('new_day_number')
            new_times = request.form.getlist('new_visit_time')
            new_urls = request.form.getlist('new_location_url')

            for dname, dtext, dday, dtime, durl in zip(new_names, new_texts, new_days, new_times, new_urls):
                if dname:  # 名前が空でなければ保存
                    cursor.execute("""
                        INSERT INTO travel_details (travel_data_id, detail_name, detail_text, day_number, visit_time, location_url)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (travel_id, dname, dtext, dday, dtime, durl))

            conn.commit()
            flash("旅行情報と詳細を更新しました")
            return redirect(url_for('my_travel.my_travel'))

        except Exception as e:
            conn.rollback()
            print(traceback.format_exc())
            flash("更新に失敗しました")

    # GETリクエスト：表示
    cursor.execute("SELECT * FROM travel_data WHERE id = ? AND u_id = ?", (travel_id, user_id))
    post = cursor.fetchone()

    cursor.execute("SELECT * FROM travel_details WHERE travel_data_id = ? ORDER BY day_number", (travel_id,))
    details = cursor.fetchall()

    conn.close()

    if not post:
        flash("指定された旅行情報が見つかりません")
        return redirect(url_for('my_travel.my_travel'))

    return render_template('edit.html', user_id=user_id, username=username, post=post, details=details)
