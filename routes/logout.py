from flask import session, redirect, url_for, Blueprint

logout_bp = Blueprint('auth', __name__)

@logout_bp.route('/logout')
def logout():
    session.clear()  # セッションをクリア
    return redirect(url_for('login.login'))  # ログインページへリダイレクト
