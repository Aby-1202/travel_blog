from flask import Flask
from routes import (
    login_bp,
    registration_bp,
    home_bp,
    logout_bp,
    input_bp
)

app = Flask(__name__, template_folder='templates', static_folder='static')

# 🔒 セッションなどに必要なシークレットキーを設定
app.secret_key = 'your_secret_key_here'  # ← 好きなランダムな文字列でOK

# Blueprintの登録
app.register_blueprint(login_bp)
app.register_blueprint(registration_bp)
app.register_blueprint(home_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(input_bp)

if __name__ == '__main__':
    app.run(debug=True)
