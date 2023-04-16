from flask import Blueprint, request, jsonify, make_response
import json
from src import db


employee_jacob_blueprint = Blueprint('employee_jacob_blueprint', __name__)

# Test the orders route
@employee_jacob_blueprint.route('/', methods=['GET'])
def test_route():
  return "<h1>This is a test for employee Jacob</h1>"

# [Jacob-1]
# Get all the orders of restaurant with Id 6
@employee_jacob_blueprint.route('/orders', methods=['GET'])
def get_orders():
  # get a cursor object from the database
  cursor = db.get_db().cursor()

  # use cursor to query the database for a list of orders
  cursor.execute('SELECT * FROM Orders WHERE restaurant_id = 6 ORDER BY order_time ASC')

  # grab the column headers from the returned data
  column_headers = [x[0] for x in cursor.description]

  # create an empty dictionary object to use in 
  # putting column headers together with data
  json_data = []

  # fetch all the data from the cursor
  theData = cursor.fetchall()

  # for each of the rows, zip the data elements together with
  # the column headers. 
  for row in theData:
      json_data.append(dict(zip(column_headers, row)))

  return jsonify(json_data)
