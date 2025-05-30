from flask import Blueprint, render_template
from flask import request
import sqlite3

login_bp = Blueprint('login', __name__)
@login_bp.route('/', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # データベース接続
        conn = sqlite3.connect('travel_blog.db')
        cursor = conn.cursor()
        
        # ユーザー登録
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        
        conn.close()
        
    return render_template('registration.html')