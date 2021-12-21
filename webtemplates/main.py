import logging
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import pymysql
import json
import datetime
from google.auth.transport import requests
from google.cloud import datastore
import google.oauth2.id_token
from flask import Flask, render_template, request, jsonify,redirect


#SQL connection
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


app = Flask(__name__)
@app.route('/')

#Render main templates
@app.route('/home')
def home():
 user=get_user()
 message=main()
 return render_template('home.html',data=user, msg=message)

@app.route('/products')
def products():
 return render_template('products.html')

@app.route('/contact')
def contact():
 return render_template('contact.html')

@app.route('/register')
def form():
 return render_template('register.html')

@app.errorhandler(500)
def server_error(e):
 # Log the error and stacktrace.
 logging.exception('An error occurred during a request.')
 return 'An internal error occurred.', 500

@app.errorhandler(404)
def page_not_found(error):
 return render_template('404.html'), 404

#get data from MongoDB
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


#SQL connection
def main():
    # When deployed to App Engine, the `GAE_ENV` environment variable will be
    # set to `standard`
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        # If running locally, use the TCP connections instead
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)

    try:
        with cnx.cursor() as cursor:
            cursor.execute('select welcome_txt from welcome_tbl;')
            result = cursor.fetchall()
            current_msg = result[0][0]
        cnx.close()

        return str(current_msg)
    except Exception as exce:
        return str(exce)
# [END gae_python37_cloudsql_mysql]

if __name__ == '__main__':
 # Only run for local development.
 app.run(host='127.0.0.1', port=8080, debug=True)
