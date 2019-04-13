from flask import Flask
from flask import Response
from flask import render_template
from flask import Blueprint
# from flask import request
from flask import request, jsonify
import uuid
import json
# from app import app, mongo
from pymongo import MongoClient
from bson import json_util
from flask import redirect

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'DB'
COLLECTION_LINK="Service"

class flaskLocal(Flask):
	def process_response(self, response):
		return(response)

app = flaskLocal(__name__)

#app.config.SERVER_NAME = 'asrez.base:80'
#app.config

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/single')
def single():
	return render_template('single.html')

@app.route('/projects/')
def projects():
	return 'The project(s) page'

@app.route('/about')
def about():
	return 'The about page'
# doc_count = col.count_documents(filter, skip=skip)
# results = col.find(filter).sort(sort).skip(skip).limit(limit)

@app.route('/scanmail/', methods=['GET','POST'], defaults={'email':None})
@app.route('/scanmail/<string:email>/',methods=['GET'])
def scanmail(email):
	mainSite="http://asrez.base/"
	site="http://asrez.base/scanmail/"
	if email == None or email == '':
		if request.method == "GET":
			return render_template('scanmail_index.html', method=request.method, random=uuid.uuid4().hex.upper()[0:7].lower(), site=site, mainSite=mainSite)
		else:
			email=request.form.get("email")
			if email:
				exists = validate_email(email)
				if exists == True:
					message="Exists!"
					status=True
					return render_template('scanmail_index.html', message=message, method=request.method, email=email, status=status, site=site, mainSite=mainSite)
				elif exists == False:
					status=False
					message="Not Exits!"
					return render_template('scanmail_index.html', message=message, method=request.method, email=email, status=status, site=site, mainSite=mainSite)
				else:
					status=False
					message="Not Sure!"
					return render_template('scanmail_index.html', message=message, method=request.method, email=email, status=status, site=site, mainSite=mainSite)
			else:
				status=False
				message="Values not enough!"
				return render_template('scanmail_index.html', message=message, method=request.method, email=email, status=status, site=site, mainSite=mainSite)
	elif email == "api":
		return render_template('scanmail_api.html', site=site, mainSite=mainSite)
	else:
		return "Error!"

if __name__ == '__main__':
	connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
	collectionLink = connection[DB_NAME][COLLECTION_LINK]
	# app.run(host='asrez.com', port=80, debug=False)
	app.run(port=80)
