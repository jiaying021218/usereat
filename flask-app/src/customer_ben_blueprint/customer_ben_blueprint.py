from flask import Blueprint, request, jsonify, make_response
import json
from src import db


customer_ben_blueprint = Blueprint('customer_ben_blueprint', __name__)

# Test the customer Ben route
@customer_ben_blueprint.route('/', methods=['GET'])
def test_route():
  return "<h1>This is a test for customer Ben</h1>"

# Get all the New York restaurants from the database
@customer_ben_blueprint.route('/restaurants', methods=['GET'])
def get_restaurants():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of restaurants
    cursor.execute(
      '''SELECT * 
      FROM Restaurants JOIN Restaurants_Locations ON Restaurants.restaurant_id = Restaurants_Locations.restaurant_id 
      WHERE Restaurants_Locations.city = \'New York\'''')

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
