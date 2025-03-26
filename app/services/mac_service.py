import requests
import os
from app.helpers import BSSIDApple_pb2
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "outputData"))
unicode = str


def getDataAddresses(data):
	query = data.lower()
	maclocs = None
	try:
		maclocs = QueryBSSID(f"{query}", more_results=True)
		if len(maclocs) < 10:
			return 'NoResult'
	except Exception as ex:
		print(f'getDataAddresses - {ex}')
		return 'Error'

	return maclocs


def getQurryAddress(query):
	lat = query[0]
	lon = query[1]

	headers = {
		'User-Agent': 'OneeetApp/1.0 (asd@yaho.com)'
	}
	try:
		response = requests.get(f'https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=10', headers=headers)
		data_json = response.json()
		address_data = f"{data_json['address']['country']}, {data_json['address']['state']}, {data_json['address']['county']}"
		return address_data
	except Exception as ex:
		print(f'Ошибка getQuerryAddress - {ex}')
		return 'Error'


def padBSSID(bssid):
	result = ''
	for e in bssid.split(':'):
		if len(e) == 1:
			e='0%s'%e
		result += e+':'
	return result.strip(':')


def ListWifiLocsApple(wifi_list):
	apdict = {}
	for wifi in wifi_list.wifi:
		if wifi.HasField('location'):
			lat=wifi.location.latitude*pow(10,-8)
			lon=wifi.location.longitude*pow(10,-8)

			mac=padBSSID(wifi.bssid)
			apdict[mac] = (lat,lon)
	return apdict


def QueryBSSID(query, more_results=True):
	list_wifi = BSSIDApple_pb2.BlockBSSIDApple()
	if type(query) in (str,unicode):
		bssid_list = [query]
	elif type(query) == list:
		bssid_list = query
	else:
		raise TypeError('Provide 1 BSSID as string or multiple BSSIDs as list of strings')
	for bssid in bssid_list:
		wifi = list_wifi.wifi.add()
		wifi.bssid = bssid
	if more_results:
		list_wifi.return_single_result = 0 # last byte in request == 0 means return ~400 results, 1 means only return results for BSSIDs queried
	else:
		list_wifi.return_single_result = 1
	ser_list_wifi = list_wifi.SerializeToString()
	length_ser_list_wifi = len(ser_list_wifi)
	headers = {'Content-Type':'application/x-www-form-urlencoded', 'Accept':'*/*', "Accept-Charset": "utf-8","Accept-Encoding": "gzip, deflate",\
			"Accept-Language":"en-us", 'User-Agent':'locationd/1753.17 CFNetwork/711.1.12 Darwin/14.0.0'}
	data = "\x00\x01\x00\x05"+"en_US"+"\x00\x13"+"com.apple.locationd"+"\x00\x0a"+"8.1.12B411"+"\x00\x00\x00\x01\x00\x00\x00" + chr(length_ser_list_wifi) + ser_list_wifi.decode();
	r = requests.post('https://gs-loc.apple.com/clls/wloc',headers=headers,data=data,verify=False) # CN of cert on this hostname is sometimes *.ls.apple.com / ls.apple.com, so have to disable SSL verify
	list_wifi = BSSIDApple_pb2.BlockBSSIDApple()
	list_wifi.ParseFromString(r.content[10:])
	return ListWifiLocsApple(list_wifi)


def DataBaseChecker(query):
	data_check ={}
	check_apple_data_base = QueryBSSID(query, more_results=False)
	apple_mac_address = list(check_apple_data_base.keys())
	print(apple_mac_address)
	if len(apple_mac_address) >= 2:
		data_check.update({"Apple": {apple_mac_address[0]: check_apple_data_base[apple_mac_address[0]]}})
		data_json = {
		  "considerIp": "false",
		  "wifiAccessPoints": [
			{
			  "macAddress": apple_mac_address[0],
			  "signalStrength": -35,
			  "signalToNoiseRatio": 0
			},
			{
			  "macAddress": apple_mac_address[1],
			  "signalStrength": -35,
			  "signalToNoiseRatio": 0
			}
		  ]
		}
		response = requests.post('https://www.googleapis.com/geolocation/v1/geolocate?key=AI*aSy*xVyk-*3jjE32L-*ptq-iK*qN1t*G4Cc*', json=data_json)
		print(response.json())
		if response.status_code == 200:
			if len(response.json()) > 1:
				data_check.update({"Google": {apple_mac_address[0]: (response.json()['location']['lat'], response.json()['location']['lng'])}})
				return data_check
			else:
				data_check.update({"Google": {apple_mac_address[0]: ("None", "None")}})
				return data_check
		else:
			data_check.update({"Google": {apple_mac_address[0]: ("None", "None")}})
			return data_check
	else:
		return 'Not found'
