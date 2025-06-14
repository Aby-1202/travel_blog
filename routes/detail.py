from flask import Blueprint, render_template, abort, session
import sqlite3
from datetime import datetime
from .models import TravelData  # SQLAlchemyモデル

detail_bp = Blueprint('detail', __name__, url_prefix='/travel')

@detail_bp.route('/<int:travel_id>')
def detail(travel_id):
    # セッションからユーザー名を取得（未ログイン時は「ゲスト」）
    username = session.get('username', 'ゲスト')

    travel_data = TravelData.query.get_or_404(travel_id)

    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # travel_data と作成者情報を取得
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

    # travel_details 一覧を取得
    cursor.execute("""
        SELECT *
        FROM travel_details
        WHERE travel_data_id = ?
        ORDER BY day_number, visit_time
    """, (travel_id,))
    travel_details = cursor.fetchall()

    conn.close()

    # 日数の計算
    try:
        start_date = datetime.strptime(travel['start_date'], "%Y-%m-%d")
        end_date   = datetime.strptime(travel['end_date'],   "%Y-%m-%d")
        duration_days = (end_date - start_date).days + 1
    except Exception:
        duration_days = "不明"

    # travel は sqlite3.Row なので Jinja2 テンプレート上で travel.t_title などでアクセス可能
    # 必要なら辞書に変換してから duration_days を追加
    travel_dict = dict(travel)
    travel_dict['duration_days'] = duration_days

    return render_template(
        'detail.html',
        travel_data=travel_data,
        travel=travel_dict,
        travel_details=travel_details,
        duration_days=duration_days,
        username=username
    )
