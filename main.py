from flask import Flask, request
import json, cryptocode


def enc(string, key):
    return cryptocode.encrypt(string, key)

def dec(encrypt, key):
    return cryptocode.decrypt(encrypt, key)

app = Flask(__name__)
with open("config.json", "r") as f:
    config = json.load(f)
a_ip = config["allow-ip"]
if_enc = bool(config["encrypt"])
d = {}
if a_ip == [] or a_ip == "":
    raise ValueError("IP access rules required")
if isinstance(a_ip, list) == True:
    for e in a_ip:
        if e.endswith("*"):
            n = e[:-1]
            op_list = []
            for i in range(0, 256):
                op_list.append(f"{n}{i}")
            a_ip.remove(e)
            a_ip.extend(op_list)


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
        if not (ip in a_ip):
            return '<h1>401 Unauthorized</h1>', 401


@app.route('/')
def index():
    return ''


@app.route('/set')
def set():
    key = request.args.get('key')
    val = request.args.get('val')
    if key == None or val == None:
        return '<h1>422 Unprocessable Entity</h1>', 422	
    if if_enc:	
    	enckey = request.args.get('enkey')
    
    	d[key] = enc(val, enckey)
    else:
      d[key] = val
    return ''


@app.route('/get')
def get():

    key = request.args.get('key')
    if key == None:
        return '<h1>422 Unprocessable Entity</h1>', 422
    try:
        _ = d[key]
    except KeyError:
        return '<h1>422 Unprocessable Entity</h1>' 
    if if_enc:
      enk = request.args.get('enkey')
      res = str(dec(d[key], enk))
      return res if res != "False" else "bad   encryption key"
    else:
      return d[key]


@app.route('/all')
def all():
    enk = request.args.get('enkey')
    r = ''
    for k, v in d.items():
        res = dec(v, enk) if dec(v, enk) != False else "bad encryption key"
        r += f"{k}:{res}<br>"
    return r


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/del")
def delkey():
    key = request.args.get('key')
    del d[key]
    return ''


app.run(host='0.0.0.0', port=5000)
