#!/usr/bin/env python

import shelve
from subprocess import check_output
import flask
from flask import request
from flask import make_response
import os
from os import environ
import string
import random
import Cookie
import datetime
import json
import io

app = flask.Flask(__name__)
app.debug = True

clicks = {}
db = {}

@app.errorhandler(404)
def page_not_found(e):
	return flask.render_template('404.html'), 404
	
@app.route('/')
def index():
	user_agent = flask.request.user_agent.browser		
	numentries = 0
	for x in db.keys():
		app.logger.debug("Short = " + x + " : URL = " + db[x])
		numentries = numentries + 1
	
	resp = make_response(flask.render_template(
		'index.html',
		db=db,
		clicks=clicks,
		numentries=numentries,	
		))		
	# Create cookie logging visit - need to check if cookie is already set, if so, just return the id value
	my_cookie = request.cookies.get('shortener')
	app.logger.debug(my_cookie)	
	#cookie_string = os.environ.get('HTTP_COOKIE')
	# Create random string for cookie_id
	if not my_cookie:
		rand_str = ''.join(random.choice(string.ascii_lowercase) for x in range(12))
		resp.set_cookie("shortener", value=rand_str)	
		my_cookie = rand_str

	#Create datetime string
	current_datetime = str(datetime.datetime.now())
	# Create json object for this unique user, logging datetime, action, cookie_id, user_agent, and dump to log file
	logline = json.dumps({'datetime': current_datetime, 'action': 'visit', 'cookie-id': my_cookie, 'user-agent': user_agent, 'myurl': '', 'myshort': ''}, sort_keys=True)
	logfile = open('static/log.txt', 'a')
	logfile.write(logline + ',')
	logfile.close()
	
	app.logger.debug(logline)

	return resp
		
	"""return flask.render_template(
	'index.html',
	db=db,
	clicks=clicks,
	numentries=numentries,
	)"""		

@app.route("/create", methods=['PUT', 'POST'])
def create():

	mywhichshort = request.form.get('whichshort')
	myurl = request.form.get('url')
	existed = ''
	# Append http if it's not on there already
	if "http://" not in myurl and "https://" not in myurl:
		myurl = "http://" + myurl		
	
	""" Functionality of the shortcut generator: 
	1) if the user manually chose a shortcut word, map it to the URL and add to the database, even if it already exists
		- thought is that the user may choose to create multiple custom url's for a site. Or they made a typo the first time.
	2) if the user chooses to automatically generate a shortcut, first we check if the URL is already mapped in the system.
		- If the URL is already mapped, just return that old shortcut, with a message saying it was already found in the system.
		- If the URL is not mapped, create a new 4-letter random phrase for the shortcut.
	"""

	if mywhichshort == "manual":
		myshort = request.form.get('short')
		db[myshort] = myurl
	elif mywhichshort == "automatic":		
		if myurl not in db.values(): #the url has not yet been mapped to a shortcut
			# Create a random string of 4 letters to use as myshort.
			myshort = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for x in range(4))
			db[myshort] = myurl
		else: #the url already has an entry in the database, get that myshort val and use it.
			for fooshort, foourl in db.items():
				if foourl == myurl:
					myshort = fooshort
					existed = 'true'
	
	# Extract Cookie value
	my_cookie = request.cookies.get('shortener')
	# Get User Agent
	user_agent = flask.request.user_agent.browser
	# Create datetime string
	current_datetime = str(datetime.datetime.now())
	# Create json object for this unique user, logging datetime, action, cookie_id, user_agent
	logline = json.dumps({'datetime': current_datetime, 'action': 'create', 'cookie-id': my_cookie, 'user-agent': user_agent, 'myurl': myurl, 'myshort': myshort}, sort_keys=True)
	logfile = open('static/log.txt', 'a')
	logfile.write(logline + ',')
	logfile.close()
	
	app.logger.debug(logline)	
	
	if myshort not in clicks.keys(): #this short word is not associated in the table yet
		clicks[myshort] = 0	
	
	numentries = 0
	for x in db.keys():
		app.logger.debug("Short = " + x + " : URL = " + db[x])
		numentries = numentries + 1

	return flask.render_template(
		'index.html',
		db=db,
		clicks=clicks,
		short=myshort,
		url=myurl,
		numentries=numentries,
		existed=existed,
		success='true',
		)

	
@app.route("/<short>", methods=['GET'])
def redirect(short):
	"""Redirect the request to the URL associated =short=, otherwise return 404
	NOT FOUND"""	
	
	if short in db.keys():
		clicks[short] = clicks[short] + 1
		destination = db.get(short)
		# Extract Cookie value
		my_cookie = request.cookies.get('shortener')	
		# Get User Agent
		user_agent = flask.request.user_agent.browser
		# Create datetime string
		current_datetime = str(datetime.datetime.now())
		# Create json object for this unique user, logging datetime, action, cookie_id, user_agent
		logline = json.dumps({'datetime': current_datetime, 'action': 'redirect', 'cookie-id': my_cookie, 'user-agent': user_agent, 'myurl': destination, 'myshort': short}, sort_keys=True)
		logfile = open('static/log.txt', 'a')
		logfile.write(logline + ',')
		logfile.close()
		app.logger.debug(logline)	
		
		app.logger.debug("Redirecting to " + destination)
		return flask.redirect(destination)
	else:
		app.logger.debug("Error - shortcut " + short + " not found")
		flask.abort(404)
	

if __name__ == "__main__":
    app.run(port=int(environ['FLASK_PORT']))
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
