from flask import Blueprint, request, jsonify, make_response
import json
from src import db

# Jacob Personas
# [1] As an employee, Jacob needs to see all the orders placed for Burger Express orders by the earliest.
# [2] Jacob wants to see all of his co-workers’ information, so he can reach out to them when needed.
# [3] As an employee, Jacob needs to be able to update the order to “Ready for Pickup” when needed.
# [4] Jacob needs to add new food to the menu sometimes
# [5] Promotion sometimes happens for certain foods, so Jacob needs to update the discount.
# [6] Jacob needs to delete food that is no longer available.
# [7] Jacob just recently changed his email, so he needs to update it in the system.
# [8] One of Jacob’s co-workers is fired, so he needs to remove the co-worker from the system.

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
    Orders.order_id as "Order ID", 
    Orders.order_time as "Order Time", 
    Orders.order_status as "Status", 
    Foods.name as "Food Name", 
    Order_Items.quantity as "Quantity" 
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
    Employees.first_name as "First Name",
    Employees.last_name as "Last Name",
    Employees.email as "Email",
    Employees.phone as "Phone",
    Employees.title as "Title",
    Employees.employee_id as "ID"
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

# [Jacob-3]
# Update order status
@employee_jacob_blueprint.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # construct the update statement
    update_stmt = 'UPDATE Orders SET order_status = "Ready for Pickup" WHERE order_id = ' + str(order_id)

    # execute the query
    cursor.execute(update_stmt)

    # commit the changes to the database
    db.get_db().commit()

    # return a success message and the updated order status
    return "Success"

# [Jacob-4]
# Add new food to the menu
@employee_jacob_blueprint.route('/menus/<int:menu_id>/foods', methods=['POST'])
def add_food(menu_id):
    # get the new food details from the request
    name = request.json.get("add_name", None)
    description = request.json.get("add_description", None)
    price = request.json.get("add_price", None)
    discount = request.json.get("add_discount", None) 

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

# [Jacob-5]
# Update food discount in the menu
@employee_jacob_blueprint.route('/update_food', methods=['PUT'])
def update_food():
  # Access JSON data from the request object
  req_data = request.get_json()

  food_id = req_data['update_food_id']
  discount = req_data['update_discount']

  # Check if the food exists
  cursor = db.get_db().cursor()
  cursor.execute('SELECT * FROM Foods WHERE food_id = %s', food_id)
  food = cursor.fetchone()

  if food is None:
      return "No Food Found"

  # Update the discount
  update_food_stmt = 'UPDATE Foods SET discount = ' + str(discount) + ' WHERE food_id = ' + str(food_id)
  cursor.execute(update_food_stmt)

  # Commit the changes to the database
  db.get_db().commit()

  # Return a success message
  return "Change Successfully"

# [Jacob-6]
# Delete food in the menu
@employee_jacob_blueprint.route('/delete_food', methods=['DELETE'])
def delete_food():
  # Access JSON data from the request object
  req_data = request.get_json()

  food_id = req_data['delete_food_id']

  # Execute the queries
  cursor = db.get_db().cursor()
  # Check if the order exists
  cursor.execute('SELECT * FROM Foods WHERE food_id = %s', food_id)
  food = cursor.fetchone()

  if food is None:
      return "No Food Found"

  # Delete the order items associated with the order
  delete_food_stmt = 'DELETE FROM Foods WHERE food_id = ' + str(food_id)
  cursor.execute(delete_food_stmt)

  # Commit the changes to the database
  db.get_db().commit()

  # Return a success message
  return "Deleted Successfully"

# [Jacob-7]
# Update employee email information
@employee_jacob_blueprint.route('/update_employee', methods=['PUT'])
def update_employee():
  req_data = request.get_json()

  employee_id = req_data['update_employee_id']
  email = req_data['update_email']

  # get a cursor object from the database
  cursor = db.get_db().cursor()
  # construct the update statement
  update_stmt = 'UPDATE Employees SET email = "' + email + '" WHERE employee_id = ' + str(employee_id)

  # execute the query
  cursor.execute(update_stmt)

  # commit the changes to the database
  db.get_db().commit()

  # return a success message
  return "Success"

# [Jacob-8]
# Delete an employee
@employee_jacob_blueprint.route('/delete_employee', methods=['DELETE'])
def delete_employee():
  req_data = request.get_json()

  employee_id = req_data['delete_employee_id']

  # get a cursor object from the database
  cursor = db.get_db().cursor()
  # construct the delete statement
  delete_stmt = 'DELETE FROM Employees WHERE employee_id = ' + str(employee_id)

  # execute the query
  cursor.execute(delete_stmt)

  # commit the changes to the database
  db.get_db().commit()

  # return a success message
  return "Delete Success"
