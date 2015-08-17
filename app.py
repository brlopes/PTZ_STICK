# roku to publish online flask: https://devcenter.heroku.com/articles/getting-started-with-python-o

from flask import Flask # Flask = microframework 
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request		# not: import requests
import json
import datetime
from flask import make_response
from options import XMLDEFAULTS 	# imports dictionary XMLDEFAULTS with positions from options.py
from flask import flash 	# flask pop-up messages


app = Flask(__name__)	# sessions in flask are crypt signed by default
app.secret_key = 'jsha@Uqweasdasd*Q(##^&@!POSDzxc'	# this is the key for the pop-session *(req)



@app.route('/')  # future main page, with option for static/video
def index():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")
	templateData = {'title' : 'HELLO!','time': timeString}
	# data = get_saved_data()
	return render_template('index.html', **templateData)
	
	
	
@app.route('/builder')  # cookies 
def builder():
	return render_template('builder.html', 
							saves=get_saved_data(),
							options=DEFAULTS
							)


# cookies return
@app.route('/save', methods=['POST'])
def save():

	flash("this is the pop from flask.flash!") # still needs html to diplay the flash
	#1 import pdb; pdb.set_trace()
	
	# on Flask, cookies are set on the response:
	response = make_response(redirect(url_for('builder')))
	
	#update with incoming data, return :
	data = get_saved_data()								# you have this information stored
	data.update(dict(request.form.items()))				# we gonna update whats changed
	response.set_cookie('character', json.dumps(data))	# and send that back ---json.dumps creates a string -->TO_JASON
	
	#actually collecting the cookie:
	# response.set_cookie('character', json.dumps(dict(request.form.items())))	#request.form returns immutable dict, items=tuple
	
	return response
	# return redirect(url_for('index')) -> returns/refresh page


def get_saved_data():
	""" get cookies from json """
	try:
		data = json.loads(request.cookies.get('character')) # takes the json string and turns to python code again --> TO_JSON
	except TypeError:
		data = {}
	return data
	
	
	
	

app.run(debug=True, host='0.0.0.0', port=8000)




#1
# >dir()
# >dir(request)
# >request.form

# JSON => dictionaries
# perv JSON: dumps = dump cookie, loads = load s(tring) cookie
