from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# dbは1回だけグローバルに作成（他のファイルからもimportして使う）
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # 必要に応じて設定を書く（例：データベースのURI）
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # ここは本番環境に応じて変更
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your_secret_key'  # 必要であればセッション用に

    # db を Flask アプリに紐付け
    db.init_app(app)

    # Blueprint 登録
    from .login import login_bp
    from .registration import registration_bp
    from .home import home_bp
    from .logout import logout_bp
    from .input import input_bp
    from .my_travel import my_travel_bp
    from .users_data import users_data_bp
    from .travel_details_input import travel_details_input_bp
    from .detail import detail_bp
    from .locations import locations_bp
    from .edit import edit_bp

    app.register_blueprint(login_bp)
    app.register_blueprint(registration_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(input_bp)
    app.register_blueprint(my_travel_bp)
    app.register_blueprint(users_data_bp)
    app.register_blueprint(travel_details_input_bp)
    app.register_blueprint(detail_bp)
    app.register_blueprint(locations_bp)
    app.register_blueprint(edit_bp)

    return app
