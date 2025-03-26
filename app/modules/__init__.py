from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Импортируем и подключаем Blueprint
from app.routes.auth import auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")
