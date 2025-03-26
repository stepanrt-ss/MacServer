from flask import Blueprint, request, send_file, abort
from app.services.auth_service import is_authorized


docks_bp = Blueprint('docks', __name__)

@docks_bp.route('/getSearchContainer', methods=['GET'])
def send_search_container():
    if is_authorized(request)[0]:
        return send_file('html/Search.html')
    else:
        abort(401)


@docks_bp.route('/getDataBaseContainer', methods=['GET'])
def send_data_base_container():
    if is_authorized(request)[0]:
        return send_file('html/DataBase.html')
    else:
        abort(401)


@docks_bp.route('/getHistoryContainer', methods=['GET'])
def send_history_container():
    if is_authorized(request)[0]:
        return send_file('html/History.html')
    else:
        abort(401)

@docks_bp.route('/getManualContainer', methods=['GET'])
def send_manual_container():
    if is_authorized(request)[0]:
        return send_file('html/Manual.html')
    else:
        abort(401)

@docks_bp.route('/getIndexContainer', methods=['GET'])
def send_index_container():
    if is_authorized(request)[0]:
        return send_file('html/Index.html')
    else:
        abort(401)
