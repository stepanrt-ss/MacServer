from flask import Blueprint

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('/get_logs', methods=['GET'])
def get_logs():
    return "Here are your logs"
