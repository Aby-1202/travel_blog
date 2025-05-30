from flask import Blueprint, render_template
from flask import request
import sqlite3

login_bp = Blueprint('login', __name__)
@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # データベース接続
        conn = sqlite3.connect('travel_blog.db')
        cursor = conn.cursor()
        
        # ユーザー認証
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        
        conn.close()
        
    return render_template('login.html')