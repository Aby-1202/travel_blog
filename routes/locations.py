from flask import Blueprint, render_template, redirect, url_for, flash, session
import sqlite3
from datetime import datetime

locations_bp = Blueprint('locations', __name__)
@locations_bp.route('/locations', methods=['GET'])
def locations():
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    username = session.get('username', 'ゲスト')

    return render_template('locations.html',user_id=user_id,username=username)

