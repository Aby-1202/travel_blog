from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash
import os

# Blueprint の定義
registration_bp = Blueprint('registration', __name__)

# 登録ページルート
@registration_bp.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['u_name']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']

        # 入力チェック
        if not username or not email or not password1 or not password2:
            flash("すべての項目を入力してください")
            return render_template('registration.html')

        if password1 != password2:
            flash("パスワードが一致しません")
            return render_template('registration.html')

        # パスワードをハッシュ化
        password_hash = generate_password_hash(password1)

        try:
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()

            # データ挿入
            cursor.execute("""
                INSERT INTO users_table (u_name, email, password_hash)
                VALUES (?, ?, ?)
            """, (username, email, password_hash))

            conn.commit()
            conn.close()
            flash("登録が完了しました")
            return redirect(url_for('login.login'))

        except sqlite3.IntegrityError:
            flash("このメールアドレスはすでに使用されています")
            return render_template('registration.html')

    return render_template('registration.html')
