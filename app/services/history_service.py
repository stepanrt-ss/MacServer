import json
import os
import csv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "users_quires"))


def get_history(user):
    user_path = f"{file_path}/{user}"
    files = [
        (el, os.path.getctime(os.path.join(user_path, el)))
        for el in os.listdir(user_path)
        if el.endswith('.csv')
    ]

    sorted_files = sorted(files, key=lambda x: x[1])  # Сортировка по времени создания

    return [el[0] for el in sorted_files]
    # return [el for el in os.listdir(f"{file_path}/{user}") if el.split('.')[-1] == 'csv']


def writeHistory(user, mac_address, query):
    if os.path.exists(f"{file_path}/{user}"):
        pass
    else:
        os.mkdir(f"{file_path}/{user}")

    with open(f"{file_path}/{user}/{query.replace(':', '')}.json", 'w', encoding='utf-8') as f:
        json.dump(mac_address, f, indent=4)

    csv_file = f"{file_path}/{user}/{query.replace(':', '')}.csv"

    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Latitude,Longitude", "BSSID"])

        for bssid, coords in mac_address.items():
            latitude, longitude = coords
            writer.writerow([f"{latitude},{longitude}", bssid])