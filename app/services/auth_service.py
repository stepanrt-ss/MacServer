import json
import os
import random
import string


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "users", "users_data.json"))


def is_authorized(request):
    cookie = request.cookies.get('Oness_key')
    print(request.cookies)
    print(cookie)
    if not cookie:
        return False, 'None'

    with open(file_path, 'r', encoding='utf-8') as f:
        data_users = json.load(f)

    for key, user_data in data_users['users'].items():
        if user_data.get('cookies_key') == cookie:
            return True, key
    return False, 'None'


def authorize(login, password):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i in data['users']:
        if i == login:
            password_check = data['users'][i]['hash_p']
            if password_check == password:
                cookie_to_set = generateCookies()
                data['users'][i]['cookies_key'] = cookie_to_set
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                return cookie_to_set
            else:
                return 'wrong password'
    else:
        return 'wrong login'

def generateCookies():
    length = 30
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return ran
