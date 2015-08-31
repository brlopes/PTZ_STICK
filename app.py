"""
flask webserver streaming mjpeg directly on html
next: 	map 2D pan on ptz
		match coord
"""
from flask import Flask # Flask = microframework 
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
import json
import datetime
from flask import make_response
from flask import flash 	# flask pop-up messages
import requests
from mjpegtools import MjpegParser


PTZ_CMD_IP = 'http://192.168.1.51/command/ptzf.cgi'

app = Flask(__name__)


@app.route('/')
def index():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")
	templateData = {'title' : 'HELLO!','time': timeString}
	return render_template('index.html', **templateData)


@app.route('/video_stream')  # ptz video stream
def video_stream():
   cam = MjpegParser(url='http://192.168.1.51/mjpeg')
   cam.quality = 20
   return cam.serve().as_flask_mjpeg()


@app.route('/ptz_control', methods=['GET', 'POST'])
def action():
    if request.method == 'POST':
        if request.form['action'] == 'left':
            r = requests.get(PTZ_CMD_IP + '?Relative=0401')
        if request.form['action'] == 'right':
            r = requests.get(PTZ_CMD_IP + '?Relative=0601')
        if request.form['action'] == 'up':
            r = requests.get(PTZ_CMD_IP + '?Relative=0801')
        if request.form['action'] == 'down':
            r = requests.get(PTZ_CMD_IP + '?Relative=0201')
    return index()

app.run(debug=True, host='0.0.0.0', port=8000)
