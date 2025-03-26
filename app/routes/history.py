from flask import Blueprint, jsonify, request, abort
from app.services.auth_service import is_authorized
from app.services.log_service import writeLogs
from app.services.mac_service import getDataAddresses, getQurryAddress
from app.services.history_service import writeHistory
from app.services.history_service import get_history


history_bp = Blueprint('history', __name__)


@history_bp.route('/getHistory', methods=['GET'])
def sendHistory():
    check_auth = is_authorized(request)
    if check_auth[0]:
        user_name = check_auth[1]
        history = get_history(user_name)
        if history:
            return jsonify({"status": "success", "history": history})
        else:
            return jsonify({"status": "success", "history": "No history"})
    else:
        abort(401)