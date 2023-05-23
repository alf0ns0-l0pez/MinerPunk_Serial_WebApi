from setup import setup
from waitress import serve
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)       
CORS(app)
setup_app=setup()

#**********************************************************
#**********************************************************
#**********************************************************
@app.route("/keepalive", methods=['GET'])
def keepalive():
    return jsonify({"status":True}), 200

@app.route("/set_relay_value", methods=['POST'])
def set_relay_value():
    return setup_app.api_response.set_relay_value(request.remote_addr, request.json), 200

@app.route("/get_relay_out", methods=['POST'])
def get_relay_out():
    return setup_app.api_response.get_relay_out(request.remote_addr, request.json), 200

@app.route("/get_sensor_inp", methods=['POST'])
def get_sensor_inp():
    return setup_app.api_response.get_sensor_inp(request.remote_addr, request.json), 200

@app.route("/get_board_description", methods=['POST'])
def get_board_description():
    return setup_app.api_response.get_board_description(request.remote_addr, request.json), 200

@app.route("/get_complete", methods=['POST'])
def get_complete():
    return setup_app.api_response.get_complete(request.remote_addr, request.json), 200

#**********************************************************
#**********************************************************
#**********************************************************
def StartConfig():
    setup_app.startup()
    StartWebServer()

def StartWebServer():
    try:
        serve(
            app, 
            host=setup_app.setup_vars['app']['ipaddr'], 
            port=setup_app.setup_vars['app']['port'])
    except Exception as e:
        setup_app.logfile.error("Web Server:{0}".format(str(e)))
#**********************************************************
#**********************************************************
#*******************************    ***************************
if __name__ == '__main__':
    StartConfig()
    