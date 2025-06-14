from flask import Blueprint, render_template, redirect, url_for, flash, session
from .models import TravelData, TravelDetail  # 必ずmodels.pyに定義されていること
from datetime import datetime

# Blueprint登録（名前の重複を避ける）
locations_details_bp = Blueprint('locations_details', __name__)

@locations_details_bp.route('/travel/<int:travel_id>')
def locations_details(travel_id):
    # ✅ セッションチェック
    if 'user_id' not in session:
        flash("ログインしてください")
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    username = session.get('username', 'ゲスト')

    # ✅ ORMで旅行データを取得
    travel = TravelData.query.get_or_404(travel_id)

    # ✅ 不正アクセス防止（他人のデータ閲覧対策）
    if travel.u_id != user_id:
        flash("この旅行データにはアクセスできません。")
        return redirect(url_for('home.home'))  # ホームなど適切なページへ

    # ✅ 紐づく詳細情報を取得
    travel_details = TravelDetail.query.filter_by(travel_id=travel_id).all()

    # ✅ 開始日・終了日が None でないことをチェック
    if travel.start_date and travel.end_date:
        duration_days = (travel.end_date - travel.start_date).days + 1
    else:
        duration_days = "不明"

    return render_template(
        "_detail.html",
        travel=travel,
        travel_details=travel_details,
        duration_days=duration_days,
        username=username
    )
