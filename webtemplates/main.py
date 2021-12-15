import logging
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json
from flask import Flask, render_template, request, jsonify,redirect


app = Flask(__name__)
@app.route('/')
@app.route('/home')
def home():
 user=get_user()
 return render_template('home.html',data=user)
@app.route('/products')
def products():
 return render_template('products.html')
@app.route('/contact')
def contact():
 return render_template('contact.html')
@app.route('/register')
def form():
 return render_template('register.html')
# [END form]
# [START submitted]
@app.route('/submitted', methods=['POST'])
def submitted_form():
 name = request.form['name']
 email = request.form['email']
 site = request.form['site_url']
 comments = request.form['comments']
 # [END submitted]
 # [START render_template]
 return render_template(
 'submitted_form.html',
 name=name,
 email=email,
 site=site,
 comments=comments)
 # [END render_template]
@app.errorhandler(500)
def server_error(e):
 # Log the error and stacktrace.
 logging.exception('An error occurred during a request.')
 return 'An internal error occurred.', 500
@app.errorhandler(404)
def page_not_found(error):
 return render_template('404.html'), 404

def get_user():
    try:
        client = MongoClient("mongodb+srv://gabbybu:0602@assignment.u61bh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

        db=client.assignment

        myCursor=db.test.find({})

        list_cur=list(myCursor)
        print(list_cur)

        json_data=dumps(list_cur)

        return json_data
    except Exception as exc:
        return str(exc)

if __name__ == '__main__':
 # Only run for local development.
 app.run(host='127.0.0.1', port=8080, debug=True)
