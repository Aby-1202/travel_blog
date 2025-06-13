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

    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # ユーザーのtravel_dataに紐づくlocationsを取得
    cursor.execute("""
        SELECT l.location_title, l.latitude, l.longitude, t.t_title
        FROM locations l
        JOIN travel_data t ON l.travel_data_id = t.id
        WHERE t.u_id = ?
    """, (user_id,))
    
    location_data = cursor.fetchall()
    conn.close()

    # PythonのデータをJavaScriptに渡すためにlistへ変換
    locations = [{
        'title': row['location_title'],
        'lat': row['latitude'],
        'lng': row['longitude'],
        'travel_title': row['t_title']
    } for row in location_data]

    return render_template('locations.html', user_id=user_id, username=username, locations=locations)
