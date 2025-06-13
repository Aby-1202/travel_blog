import traceback
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from werkzeug.utils import secure_filename

edit_bp = Blueprint('edit', __name__)

# 編集ページ表示
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
        # フォームから値を取得
        title = request.form['title']
        location = request.form['location']
        human_number = request.form['human_number']
        overview = request.form['overview']
        start_date = request.form['start_date']
        end_date = request.form['end_days']

        # 画像ファイル処理
        photo = request.files.get('photo')
        image_path = None
        if photo and photo.filename:
            filename = secure_filename(photo.filename)
            image_path = os.path.join('static/images', filename)
            photo.save(image_path)

        try:
            # UPDATE文を構築
            update_sql = """
                UPDATE travel_data
                SET t_title = ?, t_location = ?, human_number = ?, overview = ?, start_date = ?, end_date = ?
                WHERE id = ? AND u_id = ?
            """
            cursor.execute(update_sql, (title, location, human_number, overview, start_date, end_date, travel_id, user_id))

            # 画像があれば追加で更新
            if image_path:
                cursor.execute("UPDATE travel_data SET image_path = ? WHERE id = ?", (image_path, travel_id))

            conn.commit()
            flash("旅行情報を更新しました")
            return redirect(url_for('my_travel.my_travel'))

        except Exception as e:
            conn.rollback()
            print(traceback.format_exc())
            flash("更新に失敗しました")

    # GET: 編集対象のデータを取得して表示
    cursor.execute("SELECT * FROM travel_data WHERE id = ? AND u_id = ?", (travel_id, user_id))
    post = cursor.fetchone()
    conn.close()

    if not post:
        flash("指定された旅行情報が見つかりません")
        return redirect(url_for('my_travel.my_travel'))

    return render_template('edit.html', user_id=user_id, username=username, post=post)

##ここから下に前のページのtravel_dataのidを取得して、travel_dataの内容を表示するようなコードを記述する