import os
import datetime

def writeLogs(client_ip, user_name, action, query=None):
    log_string = f"[{user_name} | {client_ip} | {datetime.datetime.today()}] - {action} - {query}"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "logs", "logs.txt"))

    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(f"{log_string}\n")

