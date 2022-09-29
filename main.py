from flask import Flask, request
import json,cryptocode
def enc(string,key):
	return cryptocode.encrypt(string,key)
def dec(encrypt,key):
	return cryptocode.decrypt(encrypt,key)

app = Flask(__name__)
with open("config.json", "r") as f:
	config = json.load(f)
a_ip = config["allow-ip"]
enc_key= config['enc-key']
d = {}
print(enc_key)
if a_ip == [] or a_ip == "":
	raise ValueError("IP access rules required")
if isinstance(a_ip, list) == True:
	for e in a_ip:
		if e.endswith("*"):
			n = e[:-1]
			op_list = []
			for i in range(0,256):
				op_list.append(f"{n}{i}")
			a_ip.remove(e)	
			a_ip.extend(op_list)
print(a_ip)
@app.before_request
def before_req():
		if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
			ip = (request.environ['REMOTE_ADDR'])
		else:
			ip = (request.environ['HTTP_X_FORWARDED_FOR'])
		check = 1

		if a_ip == "*":
			check = 0
		if bool(check):	
			if not(ip in a_ip):
				return '<h1>401 Unauthorized</h1>', 401 
	
			
@app.route('/')
def index():
	return '!'
@app.route('/set')
def set():
	key = request.args.get('key')
	val = request.args.get('val')
	if key == None or val == None:
		return '<h1>422 Unprocessable Entity</h1>', 422
	d[key] = enc(val,enc_key)
	return ''
	
@app.route('/get')
def get():
	print(d)
	key = request.args.get('key')
	if key == None:
		return '<h1>422 Unprocessable Entity</h1>', 422
	try: 
		return dec(d[key],enc_key)
	except KeyError:
		return '<h1>422 Unprocessable Entity</h1>'

@app.route('/all')
def all():
	r = ''
	for k, v in d.items():
		r+=f"{k}:{dec(v,enc_key)}<br>"
	return r
	
@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


app.run(host='0.0.0.0', port=5000)
