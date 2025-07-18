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
    Nominatimの利用制限に配慮し、User-Agentと待機時間に注意。
    """
    time.sleep(1.2)  # 厳密に1秒以上待機

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


plan_input_bp = Blueprint('plan_input', __name__, url_prefix='')

# app.py と同じ BASE_DIR を使う想定。実際は app.py と同じ階層にある場合:
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # routes/ 内なら一旦 routes のパス
# ここから1階層上の project ルートに移動:
BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
DB_PATH = os.path.join(BASE_DIR, 'app.db')

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
if not os.path.isdir(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@plan_input_bp.route('/plan_input', methods=['GET', 'POST'])
def plan_input():
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    username = session.get('username', 'ゲスト')
    user_id = session['user_id']
    print(f"DEBUG: /plan_input called by user_id={user_id}")

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
            return render_template('plan_input.html', username=username)

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
                return render_template('plan_input.html', username=username)

        try:
            # 緯度経度の取得
            latitude, longitude = get_location_info(location)
            print(f"DEBUG: get_location_info({location}) -> ({latitude}, {longitude})")
            if latitude is None or longitude is None:
                flash("場所の緯度経度が見つかりませんでした")
                return render_template('plan_input.html', username=username)

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
            return render_template('plan_input.html', username=username)

    return render_template('plan_input.html', username=username)