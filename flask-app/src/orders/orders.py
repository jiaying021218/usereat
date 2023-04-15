from flask import Blueprint, request, jsonify, make_response
import json
from src import db


orders = Blueprint('orders', __name__)

# Test the Orders route
@orders.route('/', methods=['GET'])
def test_orders():
  return "<h1>This is a orders test</h1>"

# Get all the products from the database
@orders.route('/orders', methods=['GET'])
def get_orders():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT * FROM Orders')

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

  
  # Get all the orders
@orders.route('/orders/6', methods=['GET'])
def get_orders_6():
  # get a cursor object from the database
  cursor = db.get_db().cursor()

  # use cursor to query the database for a list of products
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
