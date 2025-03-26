import json
import os
from flask import Blueprint, request, jsonify, send_file, abort
from app.services.auth_service import is_authorized
from app.services.log_service import writeLogs
from app.services.mac_service import getDataAddresses, getQurryAddress
from app.services.history_service import writeHistory

mac_address_bp = Blueprint('mac_address', __name__)

@mac_address_bp.route('/getQurryAddress', methods=['POST'])
def send_mac():
    check_auth = is_authorized(request)
    if check_auth[0]:
        data_req = request.get_json()
        username = check_auth[1]
        query_address = data_req['queryAddress']
        mac_addresses = getDataAddresses(query_address)
        if mac_addresses != 'NoResult':
            writeHistory(username, mac_addresses, query_address)
            writeLogs(request.remote_addr, username, data_req.get('Action'), query_address)
            return jsonify({"length": len(mac_addresses), "query_address": getQurryAddress(query_address), "mac_addresses": mac_addresses, "status": "success"})
        else:
            return jsonify({'status': 'error', 'message': 'No result found'})
    else:
        abort(401)



@mac_address_bp.route('/getJson', methods=['POST'])
def send_json():
    check_auth = is_authorized(request)
    if check_auth[0]:
        data_req = request.get_json()
        username = check_auth[1]
        query_address = data_req['jsonName']
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "users_quires"))
        writeLogs(request.remote_addr, username, data_req.get('Action'), query_address)
        with open(f"{file_path}/{username}/{query_address.split('.')[0]}.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    else:
        abort(401)

@mac_address_bp.route('/downloadCsv', methods=['POST'])
def download_csv():
    check_auth = is_authorized(request)
    if check_auth[0]:
        data_req = request.json
        username = check_auth[1]
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "users_quires"))
        writeLogs(request.remote_addr, username, data_req.get('Action'), data_req.get('csvName'))

        file_name = data_req.get('csvName')
        path = f"{file_path}/{username}/{file_name}"
        return send_file(
            path,
            as_attachment=True,
            mimetype='text/csv',
            download_name=file_name
        )
    else:
        abort(401)

