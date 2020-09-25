from flask import Flask
from flask import request
from flask import jsonify


app = Flask(__name__)
DNS = {}

@app.route('/api/<string:name>', methods=["POST"])
def post_ip(name):
    DNS[name] = request.remote_addr
    return jsonify(DNS), 200


@app.route('/api/<string:name>', methods=["GET"])
def send_file(name, inputfile):
    #giving the ip address yourself
    if name not in DNS:
        return "Not Found", 404
    return DNS[name]


@app.route('/')
def hello():
    return "Site!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
