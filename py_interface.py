import urllib.request
import json
with open("config.json", "r") as f:
		d = json.load(f)
		global server_url
		server_url = d['url']

def get_cont(url):
	return urllib.request.urlopen(url).read().decode("utf-8") 

def get(key):
	return get_cont(server_url+f"/get?key={key}")
def set(key,value):
	get_cont(server_url+f"/set?key={key}&val={value}")
