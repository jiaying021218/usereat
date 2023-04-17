from flask import Blueprint, request, jsonify, make_response
import json
from src import db


employee_jacob_blueprint = Blueprint('employee_jacob_blueprint', __name__)

# Test the orders route
@employee_jacob_blueprint.route('/', methods=['GET'])
def test_route():
  return "<h1>This is a test for employee Jacob</h1>"

# [Jacob-1]
# Get all the orders for Burger Express at NY
@employee_jacob_blueprint.route('/orders', methods=['GET'])
def get_orders():
  # get a cursor object from the database
  cursor = db.get_db().cursor()

  # use cursor to query the database for a list of orders for Burger Express at NY
  cursor.execute(
    '''SELECT 
    Orders.order_id as \"Order ID\", 
    Orders.order_time as \"Order Time\", 
    Orders.order_status as \"Status\", 
    Foods.name as \"Food Name\", 
    Order_Items.quantity as \"Quantity\" 
    FROM Orders
    JOIN Order_Items ON Orders.order_id = Order_Items.order_id
    JOIN Foods ON Order_Items.food_id = Foods.food_id
    WHERE Orders.restaurant_location_id = 11''')

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
