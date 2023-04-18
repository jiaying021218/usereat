from flask import Blueprint, request, jsonify, make_response
import json
from src import db


customer_ben_blueprint = Blueprint('customer_ben_blueprint', __name__)

# Test the customer Ben route
@customer_ben_blueprint.route('/', methods=['GET'])
def test_route():
  return "<h1>This is a test for customer Ben</h1>"

# [Ben-1]
# Get all the New York restaurants from the database
@customer_ben_blueprint.route('/restaurants/new_york', methods=['GET'])
def get_restaurants_newyork():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of New York restaurants
    cursor.execute(
      '''SELECT Restaurants.name as \"Restaurant Name\", 
      Restaurants_Locations.address as \"Address\", 
      Restaurants_Locations.city as \"City\", 
      Restaurants_Locations.state as \"State\", 
      Restaurants_Locations.zip as \"Zip\"
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

# [Ben-2]
# Get all the New York fast food restaurants from the database
@customer_ben_blueprint.route('/restaurants/new_york/fast_food', methods=['GET'])
def get_restaurants_newyork_fastfood():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of New York fast food restaurants
    cursor.execute(
      '''SELECT Restaurants.name as \"Restaurant Name\", 
      Restaurants_Locations.address as \"Address\", 
      Restaurants_Locations.city as \"City\", 
      Restaurants_Locations.state as \"State\", 
      Restaurants_Locations.zip as \"Zip\"
      FROM Restaurants
      JOIN Restaurants_Locations ON Restaurants.restaurant_id = Restaurants_Locations.restaurant_id
      Join Categories ON Restaurants.category_id = Categories.category_id
      WHERE Restaurants_Locations.city = \'New York\' AND Categories.name = \'Fast Food\'''')

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
  
# [Ben-3]
# Get all the New York discount food from the database
@customer_ben_blueprint.route('/restaurants/new_york/discount_food', methods=['GET'])
def get_restaurants_newyork_discountfood():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of New York discount food
    cursor.execute(
      '''SELECT Foods.name as \"Name\", 
      (Foods.price - Foods.discount) as \"Discounted Price\", 
      Restaurants.name as \"Restaurants Name\" 
      FROM Restaurants
      JOIN Restaurants_Locations ON Restaurants.restaurant_id = Restaurants_Locations.restaurant_id
      JOIN Menus ON Restaurants.restaurant_id = Menus.restaurant_id
      JOIN Foods ON Menus.menu_id = Foods.menu_id
      WHERE Restaurants_Locations.city = \'New York\' AND Foods.discount > 0.00
      ORDER BY Foods.price - Foods.discount ASC''')

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


# [Ben-4]
# Get the menu of Burger Express from the database
@customer_ben_blueprint.route('/restaurants/<int:restaurant_id>/menu', methods=['GET'])
def get_burgerexpress_menu(restaurant_id):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for the menu of Burger Express
    cursor.execute(
      '''SELECT 
      Foods.name as \"Name\", 
      Foods.price as \"Price\"
      FROM Restaurants
      JOIN Menus ON Restaurants.restaurant_id = Menus.restaurant_id
      JOIN Foods ON Menus.menu_id = Foods.menu_id
      WHERE Restaurants.restaurant_id = %s''', restaurant_id)

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

# [Ben-5]
# Get all orders placed by a customer
@customer_ben_blueprint.route('/customers/<int:customer_id>/orders', methods=['GET'])
def get_customer_id_orders(customer_id):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of orders placed by the customer
    cursor.execute(
        '''SELECT Orders.order_id as "Order ID",
        Orders.order_time as "Order Time",
        Orders.order_status as "Order Status",
        Orders.restaurant_location_id as "Restaurant Location ID",
        Orders.restaurant_id as "Restaurant ID",
        Orders.customer_address_id as "Customer Address ID",
        Orders.ETA as "ETA",
        Orders.price as "Total Price"
        FROM Orders
        WHERE Orders.customer_id = %s
        ORDER BY Orders.order_time DESC''', (customer_id,))

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
