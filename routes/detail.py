from flask import Blueprint, render_template, abort, session
import sqlite3
from datetime import datetime
import re

detail_bp = Blueprint('detail', __name__, url_prefix='/travel')

# 漢数字変換用マップ
KANJI_NUM_MAP = {
    '〇': 0, '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
    '五': 5, '六': 6, '七': 7, '八': 8, '九': 9
}
KANJI_UNIT_MAP = {
    '十': 10, '百': 100, '千': 1000, '万': 10000
}

def kanji_to_int(kanji):
    """
    漢数字（簡易）を整数に変換（例：三千五百→3500）
    """
    total = 0
    num = 0
    unit = 1
    temp = 0

    unit_map = {'十': 10, '百': 100, '千': 1000, '万': 10000}
    num_map = {'〇': 0, '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
               '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}

    kanji = kanji.strip()

    for char in kanji:
        if char in num_map:
            temp = num_map[char]
        elif char in unit_map:
            if temp == 0:
                temp = 1
            total += temp * unit_map[char]
            temp = 0
        else:
            return None  # 不明な文字
    total += temp
    return total


def extract_total_cost_from_text(text):
    total = 0

    # 1. アラビア数字の金額抽出（例：3,000円）
    matches = re.findall(r'(\d{1,3}(?:,\d{3})*|\d+)\s*円', text)
    for match in matches:
        num = int(match.replace(',', ''))
        total += num

    # 2. 漢数字の金額抽出（例：三千円、五百円）
    kanji_matches = re.findall(r'([一二三四五六七八九十百千万〇零]+)円', text)
    for kmatch in kanji_matches:
        num = kanji_to_int(kmatch)
        if num:
            total += num

    return total
@detail_bp.route('/<int:travel_id>')
def detail(travel_id):
    username = session.get('username', 'ゲスト')

    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 旅行情報取得
    cursor.execute("""
        SELECT travel_data.*, users_table.u_name AS username
        FROM travel_data
        JOIN users_table ON travel_data.u_id = users_table.id
        WHERE travel_data.id = ?
    """, (travel_id,))
    travel = cursor.fetchone()

    if travel is None:
        conn.close()
        abort(404)

    # 詳細取得
    cursor.execute("""
        SELECT *
        FROM travel_details
        WHERE travel_data_id = ?
        ORDER BY day_number, visit_time
    """, (travel_id,))
    travel_details = cursor.fetchall()
    conn.close()

    # 旅行日数計算
    try:
        start_date = datetime.strptime(travel['start_date'], "%Y-%m-%d")
        end_date   = datetime.strptime(travel['end_date'],   "%Y-%m-%d")
        duration_days = (end_date - start_date).days + 1
    except Exception:
        duration_days = "不明"

    # 🔽 金額合計の計算（travel_detailsのtextから）
    total_cost = 0
    for detail in travel_details:
        text = detail['detail_text'] or ''
        total_cost += extract_total_cost_from_text(text)

    return render_template(
        'detail.html',
        travel=dict(travel),
        travel_details=travel_details,
        duration_days=duration_days,
        total_cost=total_cost,
        username=username
    )
