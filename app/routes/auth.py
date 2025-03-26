from flask import Blueprint, request, jsonify
from app.services.auth_service import authorize

auth_bp = Blueprint('auth', __name__)  # Создаём Blueprint

@auth_bp.route('/login', methods=['POST'])
def auth():
    data_request = request.json
    login = data_request.get('login')
    password = data_request.get('password')


    check_auth = authorize(login, password)
    print(check_auth)
    if check_auth == 'wrong login':
        return jsonify({'status': 'wrong login'})
    elif check_auth == 'wrong password':
        return jsonify({'status': 'wrong password'})
    elif check_auth == 'invalid sub':
        return jsonify({'status': 'invalid sub'})
    else:
        return jsonify({'status': 'success', 'cookie': check_auth, 'sub_days': checkSub(login)[1]})

