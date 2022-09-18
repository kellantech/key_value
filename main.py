from flask import Flask, request

app = Flask(__name__)

d = {}
@app.route('/')
def index():
    return '!'
@app.route('/set')
def set():
	
	key = request.args.get('key')
	val = request.args.get('val')
	if key == None or val == None:
		return '<h1>422 Unprocessable Entity</h1>', 422
	d[key] = val
	print(d)
	return ''
@app.route('/get')
def get():
	key = request.args.get('key')
	if key == None:
		return '<h1>422 Unprocessable Entity</h1>', 422
	return d[key]
		
app.run(host='0.0.0.0', port=81)
