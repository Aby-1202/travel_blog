from flask import Flask, render_template, request, Blueprint
import sqlite3
import numpy as np

app = Flask(__name__)
search_travel_bp = Blueprint('search_travel', __name__)

# DBから投稿全件取得
def get_all_travels():
    conn = sqlite3.connect('travel_data.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t_id, t_title, t_location, human_number, overview, 
               julianday('now') - julianday(t_created_at) as duration_days
        FROM travel_table
    """)
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/search_travel', methods=['GET', 'POST'])
def search_travel():
    if request.method == 'POST':
        # 入力取得
        location = request.form.get('location', '')
        human_number = request.form.get('human_number', '')
        overview = request.form.get('overview', '')
        duration = request.form.get('duration', '')

        # 入力を1つの文章に
        input_text = f"{location} 人数:{human_number} 概要:{overview} 滞在日数:{duration}"

        # DBから投稿データ取得
        records = get_all_travels()
        if not records:
            return render_template("results.html", results=[])

        ids, texts, original_data = [], [], []

        for row in records:
            t_id, title, loc, num, ov, dur = row
            doc = f"{loc} 人数:{num} 概要:{ov} 滞在日数:{int(dur)}"
            ids.append(t_id)
            texts.append(doc)
            original_data.append({
                "title": title,
                "location": loc,
                "human_number": num,
                "overview": ov
            })

        return render_template("results.html", results=original_data, input_text=input_text, ids=ids, texts=texts)

    return render_template("search_travel.html")