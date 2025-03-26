from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Импорт и регистрация Blueprint'ов
from app.routes.auth import auth_bp
from app.routes.logs import logs_bp
from app.routes.docks import docks_bp
from app.routes.mac_address import mac_address_bp
from app.routes.history import history_bp
from app.routes.data_base import dataBase_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(logs_bp, url_prefix="/logs")
app.register_blueprint(mac_address_bp, url_prefix="/mac_address")
app.register_blueprint(docks_bp, url_prefix="/docks")
app.register_blueprint(history_bp, url_prefix="/history")
app.register_blueprint(dataBase_bp, url_prefix="/dataBase")
