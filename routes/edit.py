import traceback
import time
import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from werkzeug.utils import secure_filename

edit_bp = Blueprint('edit', __name__)

def get_location_info(location_name):
    time.sleep(1.2)  # API制限に配慮
    try:
        url = 'https://nominatim.openstreetmap.org/search'
        params = {
            'q': location_name,
            'format': 'json',
            'limit': 1
        }
        headers = {
            'User-Agent': 'shabaspi-travel-map/1.0 (contact: your_email@example.com)'
        }
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon
        else:
            print(f"[INFO] 緯度経度が見つかりませんでした: {location_name}")
            return None, None
    except requests.exceptions.HTTPError as e:
        print(f"[HTTPエラー] {e} ({response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"[通信エラー] {e}")
    except Exception as e:
        print(f"[エラー] 位置情報取得失敗: {e}")
    return None, None

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
            title = request.form['title']
            location = request.form['location']
            human_number = request.form['human_number']
            overview = request.form['overview']
            start_date = request.form['start_date']
            end_date = request.form['end_days']

            photo = request.files.get('photo')
            image_path = None
            if photo and photo.filename:
                filename = secure_filename(photo.filename)
                image_path = os.path.join('static/images', filename)
                photo.save(image_path)

            update_sql = """
                UPDATE travel_data
                SET t_title = ?, t_location = ?, human_number = ?, overview = ?, start_date = ?, end_date = ?
                WHERE id = ? AND u_id = ?
            """
            cursor.execute(update_sql, (title, location, human_number, overview, start_date, end_date, travel_id, user_id))

            if image_path:
                cursor.execute("UPDATE travel_data SET image_path = ? WHERE id = ?", (image_path, travel_id))

            # t_locationから緯度経度を再取得し、locationsテーブルを更新
            lat, lng = get_location_info(location)
            if lat is not None and lng is not None:
                cursor.execute("DELETE FROM locations WHERE travel_data_id = ?", (travel_id,))
                cursor.execute("""
                    INSERT INTO locations (location_title, travel_data_id, latitude, longitude)
                    VALUES (?, ?, ?, ?)
                """, (location, travel_id, lat, lng))

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

            delete_ids = request.form.getlist('delete_detail')
            for delete_id in delete_ids:
                cursor.execute("DELETE FROM travel_details WHERE id = ? AND travel_data_id = ?", (delete_id, travel_id))

            new_names = request.form.getlist('new_detail_name')
            new_texts = request.form.getlist('new_detail_text')
            new_days = request.form.getlist('new_day_number')
            new_times = request.form.getlist('new_visit_time')
            new_urls = request.form.getlist('new_location_url')

            for dname, dtext, dday, dtime, durl in zip(new_names, new_texts, new_days, new_times, new_urls):
                if dname:
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

    cursor.execute("SELECT * FROM travel_data WHERE id = ? AND u_id = ?", (travel_id, user_id))
    post = cursor.fetchone()
    cursor.execute("SELECT * FROM travel_details WHERE travel_data_id = ? ORDER BY day_number", (travel_id,))
    details = cursor.fetchall()
    conn.close()

    if not post:
        flash("指定された旅行情報が見つかりません")
        return redirect(url_for('my_travel.my_travel'))

    return render_template('edit.html', user_id=user_id, username=username, post=post, details=details)
