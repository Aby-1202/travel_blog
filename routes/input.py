import traceback
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
import sqlite3
import os
from werkzeug.utils import secure_filename



import requests
import time

def get_location_info(location_name):
    """
    入力された地名から緯度・経度を取得する関数。

    Parameters:
        location_name (str): 地名（例："東京タワー"）

    Returns:
        tuple: (緯度, 経度) 取得できなかった場合は (None, None)
    """
    time.sleep(1)  # Nominatim APIの利用制限に配慮して1秒待機

    try:
        url = 'https://nominatim.openstreetmap.org/search'
        params = {
            'q': location_name,
            'format': 'json',
            'limit': 1
        }
        headers = {
            'User-Agent': 'travel-blog-app (your_email@example.com)'  # 任意の連絡先に変更可
        }

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon
        else:
            return None, None

    except Exception as e:
        print(f"[エラー] 位置情報取得失敗: {e}")
        return None, None


input_bp = Blueprint('input', __name__, url_prefix='')

# app.py と同じ BASE_DIR を使う想定。実際は app.py と同じ階層にある場合:
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # routes/ 内なら一旦 routes のパス
# ここから1階層上の project ルートに移動:
BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
DB_PATH = os.path.join(BASE_DIR, 'app.db')

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
if not os.path.isdir(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@input_bp.route('/input', methods=['GET', 'POST'])
def input():
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    username = session.get('username', 'ゲスト')
    user_id = session['user_id']
    print(f"DEBUG: /input called by user_id={user_id}")

    if request.method == 'POST':
        title = request.form.get('title')
        location = request.form.get('location')
        human_number = request.form.get('human_number')
        overview = request.form.get('overview')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        # 必須項目チェック
        if not title or not location or not human_number or not start_date or not end_date:
            flash("タイトル、場所、人数、開始日、終了日は必須です")
            return render_template('input.html', username=username)

        # 画像ファイルの処理
        image_filename = None
        file = request.files.get('image')
        if file and file.filename:
            original_name = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, original_name)
            try:
                file.save(save_path)
                image_filename = original_name
                print(f"DEBUG: 画像保存成功: {save_path}")
            except Exception:
                traceback.print_exc()
                flash("画像の保存に失敗しました")
                return render_template('input.html', username=username)

        try:
            # 緯度経度の取得
            latitude, longitude = get_location_info(location)
            print(f"DEBUG: get_location_info({location}) -> ({latitude}, {longitude})")
            if latitude is None or longitude is None:
                flash("場所の緯度経度が見つかりませんでした")
                return render_template('input.html', username=username)

            # DB接続：絶対パスを使う
            conn = sqlite3.connect(DB_PATH)
            # 外部キー制約を有効にする場合:
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # travel_data に挿入
            cursor.execute("""
                INSERT INTO travel_data (t_title, t_location, human_number, overview, start_date, end_date, image_path, u_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (title, location, human_number, overview, start_date, end_date, image_filename, user_id))
            travel_data_id = cursor.lastrowid
            print(f"DEBUG: travel_data INSERT OK, id={travel_data_id}")

            # locations に挿入
            cursor.execute("""
                INSERT INTO locations (location_title, travel_data_id, latitude, longitude)
                VALUES (?, ?, ?, ?)
            """, (location, travel_data_id, latitude, longitude))
            print(f"DEBUG: locations INSERT OK for travel_data_id={travel_data_id}")

            conn.commit()
            conn.close()

            flash("旅の投稿が完了しました！")
            return redirect(url_for('my_travel.my_travel'))  # 完了後はMYトラベルに飛ぶなど
        except Exception as e:
            error_trace = traceback.format_exc()
            print("ERROR TRACEBACK:\n", error_trace)
            flash(f"エラーが発生しました: {e}")
            # 失敗時にも DB_PATH が正しいかなどログに出しておく
            print(f"DEBUG: 使用 DB_PATH = {DB_PATH}")
            return render_template('input.html', username=username)

    return render_template('input.html', username=username)