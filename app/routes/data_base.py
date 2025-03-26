from flask import  request, jsonify, Blueprint, abort
from app.services.auth_service import is_authorized
from app.services.log_service import writeLogs
from app.services.mac_service import DataBaseChecker

dataBase_bp = Blueprint('dataBase', __name__)


@dataBase_bp.route('/checkDataBase', methods=['POST'])
def sendDataCheck():
    auth_check = is_authorized(request)
    if auth_check[0]:
        data_req = request.json
        mac_address = data_req['queryAddress']
        username = auth_check[1]
        writeLogs(request.remote_addr, username, data_req['Action'], mac_address)
        mac_check = DataBaseChecker(mac_address)
        if mac_check == 'Not found':
            return jsonify({"status": "success", "data": "Not found"})
        else:
            return jsonify({"status": "success", "data": mac_check})
    else:
        abort(401)
