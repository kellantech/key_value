# key_value


A key value store. 

Host yourself with waitress
 
how to run:
```
https://github.com/kellantech/key_value.git
cd key_value
python3 -m venv venv
. venv/bin/activate
pip install waitress
pip install flask
waitress-serve --host 127.0.0.1 --call main:create_app
```
