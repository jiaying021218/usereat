from flask import Blueprint, request, jsonify, make_response
import json
from src import db


employee_jacob_blueprint = Blueprint('employee_jacob_blueprint', __name__)

# Test the employee Jacob route
@employee_jacob_blueprint.route('/', methods=['GET'])
def test_route():
  return "<h1>This is a test for employee Jacob</h1>"

# [Jacob-1]
# Get all the orders for Burger Express at NY
@employee_jacob_blueprint.route('/restaurants/<int:restaurant_location_id>/orders', methods=['GET'])
def get_orders(restaurant_location_id):
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
    WHERE Orders.restaurant_location_id = %s''', restaurant_location_id)

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

# [Jacob-2]
# Get all the co-workers' information
@employee_jacob_blueprint.route('/restaurants/<int:restaurant_id>/employees', methods=['GET'])
def get_employees(restaurant_id):
  # get a cursor object from the database
  cursor = db.get_db().cursor()

  # use cursor to query the database for a list of co-workers' information
  cursor.execute(
    '''SELECT
    Employees.first_name as \"First Name\",
    Employees.last_name as \"Last Name\",
    Employees.email as \"Email\",
    Employees.phone as \"Phone\",
    Employees.title as \"Title\"
    FROM Employees
    WHERE Employees.restaurant_id = %s''', restaurant_id)

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


# Update order status
@employee_jacob_blueprint.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    # get the new status for updating the order
    new_status = request.json.get("order_status", None)

    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # construct the update statement
    update_stmt = 'UPDATE Orders SET order_status = "' + new_status + '" WHERE order_id = ' + str(order_id)

    # execute the query
    cursor.execute(update_stmt)

    # commit the changes to the database
    db.get_db().commit()

    # return a success message and the updated order status
    return "Success"



# Add new food to the menu
@employee_jacob_blueprint.route('/menus/<int:menu_id>/foods', methods=['POST'])
def add_food(menu_id):
    # get the new food details from the request
    name = request.json.get("name", None)
    description = request.json.get("description", None)
    price = request.json.get("price", None)
    discount = request.json.get("discount", None)

    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # construct the insert statement
    insert_stmt = 'INSERT INTO Foods (menu_id, name, description, price, discount) VALUES (' + str(menu_id) + ', "' + name + '", "' + description + '", ' + str(price) + ', ' + str(discount) + ')'

    # execute the query
    cursor.execute(insert_stmt)

    # commit the changes to the database
    db.get_db().commit()

    # return a success message
    return "Food item added successfully"


# Update food in the menu
@employee_jacob_blueprint.route('/foods/<int:food_id>', methods=['PUT'])
def update_food(food_id):
    # get the updated food details from the request
    name = request.json.get("name", None)
    description = request.json.get("description", None)
    price = request.json.get("price", None)
    discount = request.json.get("discount", None)

    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # construct the update statement
    update_stmt = 'UPDATE Foods SET name = "' + name + '", description = "' + description + '", price = ' + str(price) + ', discount = ' + str(discount) + ' WHERE food_id = ' + str(food_id)

    # execute the query
    cursor.execute(update_stmt)

    # commit the changes to the database
    db.get_db().commit()

    # return a success message
    return "Success"


# Delete food in the menu
@employee_jacob_blueprint.route('/foods/<int:food_id>', methods=['DELETE'])
def delete_food(food_id):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # construct the delete statement
    delete_stmt = 'DELETE FROM Foods WHERE food_id = ' + str(food_id)

    # execute the query
    cursor.execute(delete_stmt)

    # commit the changes to the database
    db.get_db().commit()

    # return a success message
    return "Success"



# Update employee information
@employee_jacob_blueprint.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    # get the updated employee details from the request
    first_name = request.json.get("first_name", None)
    last_name = request.json.get("last_name", None)
    email = request.json.get("email", None)
    phone = request.json.get("phone", None)
    title = request.json.get("title", None)
    manager_id = request.json.get("manager_id", None)

    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # construct the update statement
    update_stmt = f'UPDATE Employees SET first_name = "{first_name}", last_name = "{last_name}", email = "{email}", phone = "{phone}", title = "{title}", manager_id = {manager_id} WHERE employee_id = {employee_id}'

    # execute the query
    cursor.execute(update_stmt)

    # commit the changes to the database
    db.get_db().commit()

    # return a success message
    return "Success"


# Add a new employee
@employee_jacob_blueprint.route('/restaurants/<int:restaurant_id>/employees', methods=['POST'])
def add_employee(restaurant_id):
    # get the new employee details from the request
    first_name = request.json.get("first_name", None)
    last_name = request.json.get("last_name", None)
    email = request.json.get("email", None)
    phone = request.json.get("phone", None)
    title = request.json.get("title", None)
    manager_id = request.json.get("manager_id", None)

    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # construct the insert statement
    insert_stmt = f'INSERT INTO Employees (restaurant_id, first_name, last_name, email, phone, title, manager_id) VALUES ({restaurant_id}, "{first_name}", "{last_name}", "{email}", "{phone}", "{title}", {manager_id})'

    # execute the query
    cursor.execute(insert_stmt)

    # commit the changes to the database
    db.get_db().commit()

    # return a success message
    return "Success"


# Delete an employee
@employee_jacob_blueprint.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # construct the delete statement
    delete_stmt = 'DELETE FROM Employees WHERE employee_id = ' + str(employee_id)

    # execute the query
    cursor.execute(delete_stmt)

    # commit the changes to the database
    db.get_db().commit()

    # return a success message
    return "Success"


