import traceback
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
import uuid
from werkzeug.utils import secure_filename

edit_bp = Blueprint('edit', __name__)

@edit_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    username = session.get('username', 'ゲスト')


##ここから下に前のページのtravel_dataのidを取得して、travel_dataの内容を表示するようなコードを記述する