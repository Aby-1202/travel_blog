from flask import Flask
from routes import (
    login_bp,
    registration_bp
)

app = Flask(__name__, template_folder='templates', static_folder='static')

# Blueprintの登録
app.register_blueprint(login_bp)
app.register_blueprint(registration_bp)


if __name__ == '__main__':
    app.run(debug=True)