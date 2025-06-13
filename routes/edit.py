import traceback
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
import uuid
from werkzeug.utils import secure_filename

edit_bp = Blueprint('edit', __name__)

@edit_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    username = session.get('username', 'ゲスト')

    # DBから既存投稿を取得
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM travel_data WHERE t_id = ? AND u_id = ?", (user_id , user_id))
    post = cursor.fetchone()
    conn.close()

    if not post:
        flash("投稿が見つからないか、編集権限がありません")
        return redirect(url_for('home.home'))

    # 投稿内容を辞書に変換（列順: t_id, t_title, t_location, human_number, overview, start_date, end_date, image_path, u_id）
    post_data = {
        'id': post[0],
        'title': post[1],
        'location': post[2],
        'human_number': post[3],
        'overview': post[4],
        'start_date': post[5],
        'end_date': post[6],
        'image_path': post[7]
    }

    if request.method == 'POST':
        # 入力値取得
        title = request.form.get('title')
        location = request.form.get('location')
        human_number = request.form.get('human_number')
        overview = request.form.get('overview')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if not title or not location or not human_number or not start_date or not end_date:
            flash("タイトル、場所、人数、開始日、終了日は必須です")
            return render_template('edit.html', post=post_data, username=username)

        # 新しい画像がある場合のみ処理
        new_filename = post_data['image_path']
        file = request.files.get('photo')
        if file and file.filename != '':
            new_filename = secure_filename(file.filename)
            try:
                file.save(os.path.join(file, new_filename))
            except Exception:
                traceback.print_exc()
                flash("画像の保存に失敗しました")
                return render_template('edit.html', post=post_data, username=username)

        # DB更新
        try:
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE travel_data SET 
                    t_title = ?, 
                    t_location = ?, 
                    human_number = ?, 
                    overview = ?, 
                    start_date = ?, 
                    end_date = ?, 
                    image_path = ?
                WHERE t_id = ? AND u_id = ?
            """, (title, location, human_number, overview, start_date, end_date, new_filename, user_id))

            conn.commit()
            conn.close()

            flash("投稿が更新されました")
            return redirect(url_for('my_travel.my_travel'))

        except Exception as e:
            traceback.print_exc()
            flash(f"更新中にエラーが発生しました: {e}")
            return render_template('edit.html', post=post_data, username=username)

    return render_template('edit.html', post=post_data, username=username)


