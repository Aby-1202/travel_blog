from flask import Flask
from routes import (
    login_bp,
    registration_bp,
    home_bp,
    logout_bp,
    input_bp,
    plan_bp,
    plan_input_bp,
    my_travel_bp,
    users_data_bp,
    travel_details_input_bp,
    detail_bp,
    locations_bp,
    edit_bp,
    favorite_bookmark_bp,
    search_travel_bp
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
app.register_blueprint(plan_bp)
app.register_blueprint(plan_input_bp)
app.register_blueprint(my_travel_bp)
app.register_blueprint(users_data_bp)
app.register_blueprint(travel_details_input_bp)
app.register_blueprint(detail_bp)
app.register_blueprint(locations_bp)
app.register_blueprint(edit_bp)
app.register_blueprint(favorite_bookmark_bp)
app.register_blueprint(search_travel_bp)

if __name__ == '__main__':
    app.run(debug=True)