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
    '''SELECT 
    Restaurants.name as "Restaurant Name", 
    Restaurants_Locations.address as "Address", 
    Restaurants_Locations.city as "City", 
    Restaurants_Locations.state as "State", 
    Restaurants_Locations.zip as "Zip",
    Categories.name as "Category"
    FROM Restaurants 
    JOIN Restaurants_Locations ON Restaurants.restaurant_id = Restaurants_Locations.restaurant_id 
    JOIN Categories ON Restaurants.category_id = Categories.category_id
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
# Get all the New York restaurants from the database that belongs to the given category
@customer_ben_blueprint.route('/restaurants/new_york/<int:category_id>', methods=['GET'])
def get_restaurants_newyork_category(category_id):
  # get a cursor object from the database
  cursor = db.get_db().cursor()

  # use cursor to query the database for a list of New York restaurants that belongs to the given category
  cursor.execute(
    '''SELECT 
    Restaurants.name as "Restaurant Name", 
    Restaurants_Locations.address as "Address", 
    Restaurants_Locations.city as "City", 
    Restaurants_Locations.state as "State", 
    Restaurants_Locations.zip as "Zip"
    FROM Restaurants
    JOIN Restaurants_Locations ON Restaurants.restaurant_id = Restaurants_Locations.restaurant_id
    Join Categories ON Restaurants.category_id = Categories.category_id
    WHERE Restaurants_Locations.city = \'New York\' AND Categories.category_id = %s''', category_id)

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
    '''SELECT 
    Foods.name as "Name", 
    (Foods.price - Foods.discount) as "Discounted Price", 
    Restaurants.name as "Restaurants Name" 
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
@customer_ben_blueprint.route('/menus/<int:menu_id>', methods=['GET'])
def get_menu_id(menu_id):
  # get a cursor object from the database
  cursor = db.get_db().cursor()

  # use cursor to query the database for the menu of Burger Express
  cursor.execute(
    '''SELECT 
    Foods.name as "Name", 
    Foods.price as "Price"
    FROM Restaurants
    JOIN Menus ON Restaurants.restaurant_id = Menus.restaurant_id
    JOIN Foods ON Menus.menu_id = Foods.menu_id
    WHERE Menus.menu_id = %s''', menu_id)

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
      '''SELECT 
      Orders.order_id as "Order ID",
      Orders.order_time as "Order Time",
      Orders.order_status as "Order Status",
      Orders.restaurant_location_id as "Restaurant Location ID",
      Orders.restaurant_id as "Restaurant ID",
      Orders.customer_id as "Customer ID",
      Orders.customer_address_id as "Customer Address ID",
      Orders.ETA as "ETA"
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

# [Ben-6]
# Place an order for a customer
@customer_ben_blueprint.route('/place_order', methods=['POST'])
def place_order():
  # Access JSON data from the request object
  current_app.logger.info('Processing order data')
  req_data = request.get_json()
  current_app.logger.info(req_data)

  restaurant_location_id = req_data['restaurant_location_id']
  restaurant_id = req_data['restaurant_id']

  # Insert order data into the Orders table
  insert_order_stmt = 'INSERT INTO Orders (restaurant_location_id, restaurant_id) VALUES '
  insert_order_stmt += '(1, ' + str(restaurant_location_id) + ', ' + str(restaurant_id) + ', 1)'

  current_app.logger.info(insert_order_stmt)

  # Execute the queries
  cursor = db.get_db().cursor()
  cursor.execute(insert_order_stmt)
  # Get the order_id of the inserted order
  order_id = cursor.lastrowid

  # Commit the changes to the database
  db.get_db().commit()

  # Return a success message and the order_id
  return "Success"
