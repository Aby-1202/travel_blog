import traceback
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
import uuid
from werkzeug.utils import secure_filename

input_bp = Blueprint('input', __name__, url_prefix='')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    print("DEBUG: session user_id =", user_id)

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
        if file:
            original_name = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, original_name)
            try:
                file.save(save_path)
                image_filename = original_name
            except Exception:
                traceback.print_exc()
                flash("画像の保存に失敗しました")
                return render_template('input.html', username=username)
            
        try:
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO travel_data (t_title, t_location, human_number, overview, start_date, end_date, image_path, u_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (title, location, human_number, overview, start_date, end_date, image_filename, user_id))

            conn.commit()
            conn.close()

            flash("旅の投稿が完了しました！")
            return redirect(url_for('home.home'))

        except Exception as e:
            error_trace = traceback.format_exc()
            print(error_trace)
            flash(f"エラーが発生しました: {e}")
            return render_template('input.html', username=username)

    return render_template('input.html', username=username)
