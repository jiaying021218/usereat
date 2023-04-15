-- This file is to bootstrap a database for the CS3200 project. 

-- Create a new database.  You can change the name later.  You'll
-- need this name in the FLASK API file(s),  the AppSmith 
-- data source creation.
create database usereat;

-- Via the Docker Compose file, a special user called webapp will 
-- be created in MySQL. We are going to grant that user 
-- all privilages to the new database we just created. 
grant all privileges on usereat.* to 'webapp'@'%';
flush privileges;

-- Move into the database we just created.
use usereat;

-- -------------------------------------------------------
-- Table: Employees
-- Employees.title can be
-- 'Manager'
-- 'Server'
-- 'Chief'
-- 'Cashier'
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `Employees` (
  `employee_id` integer PRIMARY KEY,
  `restaurant_id` integer NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `manager_id` integer DEFAULT NULL,
  `email` varchar(255) UNIQUE NOT NULL,
  `phone` varchar(255) UNIQUE NOT NULL,
  `title` varchar(255) NOT NULL
);

-- -------------------------------------------------------
--  Table: Restaurants
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `Restaurants` (
  `restaurant_id` integer PRIMARY KEY,
  `name` varchar(255) NOT NULL,
  `phone` varchar(255) UNIQUE NOT NULL,
  `email` varchar(255) UNIQUE NOT NULL,
  `category_id` integer DEFAULT NULL
);

-- -------------------------------------------------------
-- Table: Restaurants_Locations
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `Restaurants_Locations` (
  `restaurant_location_id` integer PRIMARY KEY,
  `restaurant_id` integer NOT NULL,
  `address` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `zip` varchar(255) NOT NULL
);

-- -------------------------------------------------------
-- Table: Categories
-- Categories.name can be
-- 'Pizza'
-- 'Fast Food'
-- 'Chinese Food'
-- 'Italian Food'
-- 'American Food'
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `Categories` (
  `category_id` integer PRIMARY KEY,
  `name` varchar(255) NOT NULL
);

-- -------------------------------------------------------
-- Table: Menus
-- Menus.name can be
-- 'Lunch'
-- 'Dinner'
-- 'Both'
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `Menus` (
  `menu_id` integer PRIMARY KEY,
  `restaurant_id` integer NOT NULL,
  `name` varchar(255) DEFAULT NULL
);

-- -------------------------------------------------------
-- Table: Foods
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `Foods` (
  `food_id` integer PRIMARY KEY,
  `menu_id` integer NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `price` decimal NOT NULL DEFAULT 0,
  `discount` decimal DEFAULT NULL
);

-- -------------------------------------------------------
-- Table: Orders
-- Orders.order_status can be
-- 'Order Received'
-- 'Waiting For Pickup'
-- 'In Delivery'
-- 'Delivered'
-- 'Canceled'
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `Orders` (
  `order_id` integer PRIMARY KEY,
  `customer_id` integer NOT NULL,
  `driver_id` integer DEFAULT NULL,
  `restaurant_location_id` integer NOT NULL,
  `restaurant_id` integer NOT NULL,
  `order_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `customer_address_id` integer NOT NULL,
  `order_status` varchar(255) NOT NULL DEFAULT 'Order Received',
  `ETA` integer DEFAULT NULL,
  `price` decimal NOT NULL
);

-- -------------------------------------------------------
-- Table: Orders_Items
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `Order_Items` (
  `order_item_id` integer PRIMARY KEY,
  `order_id` integer NOT NULL,
  `food_id` integer NOT NULL,
  `quantity` integer NOT NULL DEFAULT 1,
  `special_instructions` text DEFAULT NULL
);

-- -------------------------------------------------------
-- Table: Drivers
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `Drivers` (
  `driver_id` integer PRIMARY KEY,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(255) UNIQUE NOT NULL,
  `phone` varchar(255) UNIQUE NOT NULL
);

-- -------------------------------------------------------
-- Table: Payments
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `Payments` (
  `payment_id` integer PRIMARY KEY,
  `order_id` integer NOT NULL,
  `card_id` integer NOT NULL,
  `price` decimal NOT NULL
);

-- -------------------------------------------------------
-- Table: Cards
-- Cards.type can be
-- 'Visa'
-- 'MasterCard'
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `Cards` (
  `card_id` integer PRIMARY KEY,
  `customer_id` integer NOT NULL,
  `type` varchar(255) NOT NULL,
  `cardholder` varchar(255) NOT NULL,
  `company` varchar(255) NOT NULL,
  `card_number` varchar(255) NOT NULL,
  `expiration_date` date NOT NULL,
  `CVV` integer NOT NULL
);

-- -------------------------------------------------------
-- Table: Customers
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `Customers` (
  `customer_id` integer PRIMARY KEY,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(255) UNIQUE NOT NULL,
  `phone` varchar(255) UNIQUE NOT NULL
);

-- -------------------------------------------------------
-- Table: Customers_Locations
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `Customers_Locations` (
  `customer_address_id` integer PRIMARY KEY,
  `customer_id` integer NOT NULL,
  `address` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `zip` varchar(255) NOT NULL
);

-- -------------------------------------------------------
-- Adding Foreign Key
-- -------------------------------------------------------
ALTER TABLE `Employees` ADD FOREIGN KEY (`manager_id`) REFERENCES `Employees` (`employee_id`);

ALTER TABLE `Employees` ADD FOREIGN KEY (`restaurant_id`) REFERENCES `Restaurants` (`restaurant_id`);

ALTER TABLE `Restaurants` ADD FOREIGN KEY (`category_id`) REFERENCES `Categories` (`category_id`);

ALTER TABLE `Restaurants_Locations` ADD FOREIGN KEY (`restaurant_id`) REFERENCES `Restaurants` (`restaurant_id`);

ALTER TABLE `Menus` ADD FOREIGN KEY (`restaurant_id`) REFERENCES `Restaurants` (`restaurant_id`);

ALTER TABLE `Foods` ADD FOREIGN KEY (`menu_id`) REFERENCES `Menus` (`menu_id`);

ALTER TABLE `Orders` ADD FOREIGN KEY (`customer_id`) REFERENCES `Customers` (`customer_id`);

ALTER TABLE `Orders` ADD FOREIGN KEY (`driver_id`) REFERENCES `Drivers` (`driver_id`);

ALTER TABLE `Orders` ADD FOREIGN KEY (`restaurant_location_id`) REFERENCES `Restaurants_Locations` (`restaurant_location_id`);

ALTER TABLE `Orders` ADD FOREIGN KEY (`restaurant_id`) REFERENCES `Restaurants` (`restaurant_id`);

ALTER TABLE `Orders` ADD FOREIGN KEY (`customer_address_id`) REFERENCES `Customers_Locations` (`customer_address_id`);

ALTER TABLE `Order_Items` ADD FOREIGN KEY (`order_id`) REFERENCES `Orders` (`order_id`);

ALTER TABLE `Order_Items` ADD FOREIGN KEY (`food_id`) REFERENCES `Foods` (`food_id`);

ALTER TABLE `Payments` ADD FOREIGN KEY (`order_id`) REFERENCES `Orders` (`order_id`);

ALTER TABLE `Payments` ADD FOREIGN KEY (`card_id`) REFERENCES `Cards` (`card_id`);

ALTER TABLE `Cards` ADD FOREIGN KEY (`customer_id`) REFERENCES `Customers` (`customer_id`);

ALTER TABLE `Customers_Locations` ADD FOREIGN KEY (`customer_id`) REFERENCES `Customers` (`customer_id`);

-- -------------------------------------------------------
-- Inserting Data to Tables
-- -------------------------------------------------------

-- Categories
INSERT INTO `Categories` (`category_id`, `name`) VALUES
(1, 'Pizza'),
(2, 'Fast Food'),
(3, 'Chinese Food'),
(4, 'Italian Food'),
(5, 'American Food');

-- Customers
INSERT INTO `Customers` (`customer_id`, `first_name`, `last_name`, `email`, `phone`) VALUES
(1, 'John', 'Doe', 'john.doe@example.com', '555-123-4567'),
(2, 'Jane', 'Doe', 'jane.doe@example.com', '555-123-7654'),
(3, 'Michael', 'Smith', 'michael.smith@example.com', '555-321-9876'),
(4, 'Emily', 'Jones', 'emily.jones@example.com', '555-321-7896'),
(5, 'Jessica', 'Taylor', 'jessica.taylor@example.com', '555-987-6543'),
(6, 'Chris', 'Brown', 'chris.brown@example.com', '555-987-3456'),
(7, 'Ashley', 'Wilson', 'ashley.wilson@example.com', '555-678-1234'),
(8, 'Samantha', 'Thomas', 'samantha.thomas@example.com', '555-678-4321'),
(9, 'Sarah', 'Moore', 'sarah.moore@example.com', '555-876-2345'),
(10, 'Daniel', 'Lee', 'daniel.lee@example.com', '555-876-5432'),
(11, 'David', 'Harris', 'david.harris@example.com', '555-345-6789'),
(12, 'James', 'Clark', 'james.clark@example.com', '555-345-9876'),
(13, 'Jennifer', 'Lewis', 'jennifer.lewis@example.com', '555-234-5678'),
(14, 'Michelle', 'Walker', 'michelle.walker@example.com', '555-234-8765'),
(15, 'Robert', 'Hall', 'robert.hall@example.com', '555-567-1234'),
(16, 'Angela', 'Young', 'angela.young@example.com', '555-567-4321'),
(17, 'Melissa', 'Hernandez', 'melissa.hernandez@example.com', '555-765-2345'),
(18, 'William', 'King', 'william.king@example.com', '555-765-3456'),
(19, 'Stephanie', 'Wright', 'stephanie.wright@example.com', '555-456-7890'),
(20, 'Brian', 'Lopez', 'brian.lopez@example.com', '555-456-8907');

-- Customer_Locations
-- Customer_Locations
INSERT INTO `Customers_Locations` (`customer_address_id`, `customer_id`, `address`, `city`, `state`, `zip`) VALUES
(1, 1, '123 Main St', 'New York', 'NY', '10001'),
(2, 2, '234 Oak St', 'Los Angeles', 'CA', '90001'),
(3, 3, '345 Elm St', 'Chicago', 'IL', '60601'),
(4, 4, '456 Pine St', 'Houston', 'TX', '77001'),
(5, 5, '567 Maple St', 'Philadelphia', 'PA', '19102'),
(6, 6, '678 Cedar St', 'Phoenix', 'AZ', '85001'),
(7, 7, '789 Birch St', 'San Antonio', 'TX', '78201'),
(8, 8, '890 Walnut St', 'San Diego', 'CA', '92101'),
(9, 9, '901 Chestnut St', 'Dallas', 'TX', '75201'),
(10, 10, '1012 Redwood St', 'San Jose', 'CA', '95101'),
(11, 11, '1113 Willow St', 'Austin', 'TX', '73301'),
(12, 12, '1214 Palm St', 'Jacksonville', 'FL', '32099'),
(13, 13, '1315 Spruce St', 'Fort Worth', 'TX', '76101'),
(14, 14, '1416 Aspen St', 'Columbus', 'OH', '43085'),
(15, 15, '1517 Hickory St', 'San Francisco', 'CA', '94102'),
(16, 16, '1618 Sycamore St', 'Charlotte', 'NC', '28201'),
(17, 17, '1719 Dogwood St', 'Indianapolis', 'IN', '46201'),
(18, 18, '1820 Magnolia St', 'Seattle', 'WA', '98101'),
(19, 19, '1921 Cherry St', 'Denver', 'CO', '80201'),
(20, 20, '2022 Laurel St', 'Washington', 'DC', '20001');

-- Cards
INSERT INTO `Cards` (`card_id`, `customer_id`, `type`, `cardholder`, `company`, `card_number`, `expiration_date`, `CVV`) VALUES
(1, 1, 'Visa', 'John Doe', 'Bank of America', '4111111111111111', '2025-01-31', 123),
(2, 2, 'MasterCard', 'Jane Doe', 'Chase', '5500000000000004', '2024-09-30', 234),
(3, 3, 'Visa', 'Michael Smith', 'Wells Fargo', '4007000000027', '2025-05-31', 345),
(4, 4, 'MasterCard', 'Emily Jones', 'Citibank', '5555555555554444', '2024-12-31', 456),
(5, 5, 'Visa', 'Jessica Taylor', 'US Bank', '4012888888881881', '2025-08-31', 567),
(6, 6, 'MasterCard', 'Chris Brown', 'Capital One', '5105105105105100', '2023-06-30', 678),
(7, 7, 'Visa', 'Ashley Wilson', 'PNC Bank', '4111111111111111', '2025-02-28', 789),
(8, 8, 'MasterCard', 'Samantha Thomas', 'Bank of America', '5500000000000004', '2024-11-30', 890),
(9, 9, 'Visa', 'Sarah Moore', 'Chase', '4007000000027', '2025-06-30', 901),
(10, 10, 'MasterCard', 'Daniel Lee', 'Wells Fargo', '5105105105105100', '2023-10-31', 901),
(11, 11, 'Visa', 'David Harris', 'Citibank', '4012888888881881', '2025-07-31', 112),
(12, 12, 'MasterCard', 'James Clark', 'US Bank', '5555555555554444', '2024-02-28', 223),
(13, 13, 'Visa', 'Jennifer Lewis', 'Capital One', '4111111111111111', '2025-04-30', 334),
(14, 14, 'MasterCard', 'Michelle Walker', 'PNC Bank', '5500000000000004', '2023-08-31', 445),
(15, 15, 'Visa', 'Robert Hall', 'Bank of America', '4007000000027', '2025-03-31', 556),
(16, 16, 'MasterCard', 'Angela Young', 'Chase', '5105105105105100', '2024-01-31', 667),
(17, 17, 'Visa', 'Melissa Hernandez', 'Wells Fargo', '4012888888881881', '2025-06-30', 778),
(18, 18, 'MasterCard', 'William King', 'Citibank', '5555555555554444', '2023-07-31', 889),
(19, 19, 'Visa', 'Stephanie Wright', 'US Bank', '4111111111111111', '2025-12-31', 990),
(20, 20, 'MasterCard', 'Brian Lopez', 'Capital One', '5500000000000004', '2024-03-31', 101);

-- Drivers
INSERT INTO `Drivers` (`driver_id`, `first_name`, `last_name`, `email`, `phone`) VALUES
(1, 'Alan', 'Smith', 'alan.smith@example.com', '123-456-7890'),
(2, 'Barbara', 'Johnson', 'barbara.johnson@example.com', '123-456-7891'),
(3, 'Charles', 'Williams', 'charles.williams@example.com', '123-456-7892'),
(4, 'Donna', 'Brown', 'donna.brown@example.com', '123-456-7893'),
(5, 'Edward', 'Jones', 'edward.jones@example.com', '123-456-7894'),
(6, 'Felicity', 'Garcia', 'felicity.garcia@example.com', '123-456-7895'),
(7, 'George', 'Miller', 'george.miller@example.com', '123-456-7896'),
(8, 'Hannah', 'Davis', 'hannah.davis@example.com', '123-456-7897'),
(9, 'Ian', 'Rodriguez', 'ian.rodriguez@example.com', '123-456-7898'),
(10, 'Julia', 'Martinez', 'julia.martinez@example.com', '123-456-7899'),
(11, 'Kevin', 'Hernandez', 'kevin.hernandez@example.com', '123-456-7880'),
(12, 'Linda', 'Lopez', 'linda.lopez@example.com', '123-456-7881'),
(13, 'Michael', 'Gonzalez', 'michael.gonzalez@example.com', '123-456-7882'),
(14, 'Nancy', 'Wilson', 'nancy.wilson@example.com', '123-456-7883'),
(15, 'Oliver', 'Anderson', 'oliver.anderson@example.com', '123-456-7884'),
(16, 'Pamela', 'Thomas', 'pamela.thomas@example.com', '123-456-7885'),
(17, 'Quentin', 'Taylor', 'quentin.taylor@example.com', '123-456-7886'),
(18, 'Rachel', 'Moore', 'rachel.moore@example.com', '123-456-7887'),
(19, 'Steve', 'Jackson', 'steve.jackson@example.com', '123-456-7888'),
(20, 'Tina', 'Martin', 'tina.martin@example.com', '123-456-7889');

-- Restaurants
INSERT INTO `Restaurants` (`restaurant_id`, `name`, `phone`, `email`, `category_id`) VALUES
(1, 'Pizza Palace', '111-111-1111', 'pizza@example.com', 1),
(2, 'Fast Food Fiesta', '111-111-1112', 'fastfood@example.com', 2),
(3, 'Chinese Corner', '111-111-1113', 'chinese@example.com', 3),
(4, 'Italian Inn', '111-111-1114', 'italian@example.com', 4),
(5, 'American Diner', '111-111-1115', 'american@example.com', 5),
(6, 'Burger Express', '555-1066', 'burgerexpress@example.com', 2),
(7, 'Taco Town', '555-1077', 'tacotown@example.com', 2),
(8, 'Pasta Paradise', '555-1088', 'pastaparadise@example.com', 4),
(9, 'Sushi World', '555-1099', 'sushiworld@example.com', 5),
(10, 'Steak House', '555-1010', 'steakhouse@example.com', 5);


-- Restaurant_Locations
INSERT INTO `Restaurants_Locations` (`restaurant_location_id`, `restaurant_id`, `address`, `city`, `state`, `zip`) VALUES
(1, 1, '123 Pizza Street', 'New York', 'NY', '10001'),
(2, 1, '456 Pizza Avenue', 'Los Angeles', 'CA', '90001'),
(3, 2, '789 Fastfood Drive', 'Chicago', 'IL', '60601'),
(4, 2, '1011 Fastfood Boulevard', 'Houston', 'TX', '77001'),
(5, 3, '1213 Chinese Road', 'Phoenix', 'AZ', '85001'),
(6, 3, '1415 Chinese Plaza', 'Philadelphia', 'PA', '19101'),
(7, 4, '1617 Italian Way', 'San Antonio', 'TX', '78201'),
(8, 4, '1819 Italian Circle', 'San Diego', 'CA', '92101'),
(9, 5, '2021 American Lane', 'Dallas', 'TX', '75201'),
(10, 5, '2223 American Court', 'San Jose', 'CA', '95101'),
(11, 6, '901 Pine St', 'New York', 'NY', '10001'),
(12, 6, '902 Oak St', 'Los Angeles', 'CA', '90001'),
(13, 7, '903 Elm St', 'Chicago', 'IL', '60601'),
(14, 7, '904 Maple St', 'Houston', 'TX', '77001'),
(15, 8, '905 Cedar St', 'Phoenix', 'AZ', '85001'),
(16, 8, '906 Spruce St', 'Philadelphia', 'PA', '19019'),
(17, 9, '907 Birch St', 'San Antonio', 'TX', '78201'),
(18, 9, '908 Walnut St', 'San Diego', 'CA', '92101'),
(19, 10, '909 Chestnut St', 'Dallas', 'TX', '75201'),
(20, 10, '910 Hickory St', 'San Jose', 'CA', '95101');


-- Menus
INSERT INTO `Menus` (`menu_id`, `restaurant_id`, `name`) VALUES
(1, 1, 'Lunch'),
(2, 1, 'Dinner'),
(3, 2, 'Both'),
(4, 3, 'Lunch'),
(5, 3, 'Dinner'),
(6, 4, 'Both'),
(7, 5, 'Lunch'),
(8, 5, 'Dinner');

-- Foods
INSERT INTO `Foods` (`food_id`, `menu_id`, `name`, `description`, `price`, `discount`) VALUES
(1, 1, 'Pepperoni Pizza', 'Pepperoni, mozzarella, and tomato sauce', 10.99, NULL),
(2, 1, 'Veggie Pizza', 'Mixed vegetables, mozzarella, and tomato sauce', 9.99, 1.00),
(3, 2, 'Spaghetti Bolognese', 'Spaghetti with meat sauce', 12.99, NULL),
(4, 2, 'Fettuccine Alfredo', 'Fettuccine with creamy Alfredo sauce', 11.99, 3.00),
(5, 3, 'Cheeseburger', 'Cheeseburger with lettuce, tomato, and onion', 5.99, NULL),
(6, 3, 'Chicken Nuggets', 'Crispy chicken nuggets with dipping sauce', 4.99, NULL),
(7, 4, 'Kung Pao Chicken', 'Spicy chicken with peanuts and vegetables', 13.99, NULL),
(8, 4, 'Fried Rice', 'Classic fried rice with vegetables and egg', 8.99, 2.00),
(9, 5, 'Lasagna', 'Layers of pasta, ricotta, mozzarella, and meat sauce', 14.99, NULL),
(10, 5, 'Caesar Salad', 'Romaine lettuce, croutons, and Caesar dressing', 7.99, 1.00),
(11, 3, 'Pepperoni Pizza', 'Classic pepperoni pizza with mozzarella cheese and tomato sauce', 10.99, NULL),
(12, 3, 'Mushroom Pizza', 'Mushroom pizza with mozzarella cheese and tomato sauce', 10.99, 2.55),
(13, 3, 'Veggie Pizza', 'Vegetarian pizza with bell peppers, onions, mushrooms, olives, and tomatoes', 11.99, NULL),
(14, 3, 'BBQ Chicken Pizza', 'BBQ chicken pizza with red onion, cilantro, and BBQ sauce', 12.99, NULL),
(15, 3, 'Hawaiian Pizza', 'Hawaiian pizza with ham, pineapple, and bacon', 11.99, 3.99),
(16, 4, 'Cheeseburger', 'Classic cheeseburger with lettuce, tomato, and onion', 7.99, NULL),
(17, 4, 'Bacon Cheeseburger', 'Bacon cheeseburger with lettuce, tomato, and onion', 8.99, 1.99),
(18, 4, 'Grilled Chicken Sandwich', 'Grilled chicken sandwich with lettuce, tomato, and mayo', 7.99, NULL),
(19, 4, 'Veggie Burger', 'Vegetarian burger with lettuce, tomato, and onion', 7.99, NULL),
(20, 4, 'Fish Sandwich', 'Fish sandwich with tartar sauce, lettuce, and tomato', 7.99, 0.99);


-- Employees
INSERT INTO `Employees` (`employee_id`, `restaurant_id`, `first_name`, `last_name`, `manager_id`, `email`, `phone`, `title`) VALUES
(1, 1, 'Amanda', 'Smith', NULL, 'amanda.smith@example.com', '555-555-5551', 'Manager'),
(2, 1, 'Brad', 'Johnson', 1, 'brad.johnson@example.com', '555-555-5552', 'Server'),
(3, 1, 'Cathy', 'Williams', 1, 'cathy.williams@example.com', '555-555-5553', 'Cook'),
(4, 2, 'David', 'Brown', NULL, 'david.brown@example.com', '555-555-5554', 'Manager'),
(5, 2, 'Eva', 'Jones', 4, 'eva.jones@example.com', '555-555-5555', 'Server'),
(6, 2, 'Frank', 'Garcia', 4, 'frank.garcia@example.com', '555-555-5556', 'Cook'),
(7, 3, 'Gina', 'Miller', NULL, 'gina.miller@example.com', '555-555-5557', 'Manager'),
(8, 3, 'Henry', 'Davis', 7, 'henry.davis@example.com', '555-555-5558', 'Server'),
(9, 3, 'Ivy', 'Rodriguez', 7, 'ivy.rodriguez@example.com', '555-555-5559', 'Cook'),
(10, 4, 'Jack', 'Martinez', NULL, 'jack.martinez@example.com', '555-555-5560', 'Manager'),
(11, 4, 'Kara', 'Hernandez', 10, 'kara.hernandez@example.com', '555-555-5561', 'Server'),
(12, 4, 'Liam', 'Lopez', 10, 'liam.lopez@example.com', '555-555-5562', 'Cook'),
(13, 5, 'Mandy', 'Gonzalez', NULL, 'mandy.gonzalez@example.com', '555-555-5563', 'Manager'),
(14, 5, 'Ned', 'Wilson', 13, 'ned.wilson@example.com', '555-555-5564', 'Server'),
(15, 5, 'Olivia', 'Anderson', 13, 'olivia.anderson@example.com', '555-555-5565', 'Cook'),
(16, 6, 'Pam', 'Green', 1, 'pam.green@example.com', '555-2011', 'Manager'),
(17, 6, 'Randy', 'Martinez', 16, 'randy.martinez@example.com', '555-2012', 'Server'),
(18, 6, 'Ava', 'Morgan', 16, 'ava.morgan@example.com', '555-2013', 'Server'),
(19, 6, 'David', 'Clark', 16, 'david.clark@example.com', '555-2014', 'Chief'),
(20, 6, 'Olivia', 'Smith', 16, 'olivia.smith@example.com', '555-2015', 'Cashier'),
(21, 7, 'Tina', 'Taylor', 1, 'tina.taylor@example.com', '555-3011', 'Manager'),
(22, 7, 'Dylan', 'Cooper', 21, 'dylan.cooper@example.com', '555-3012', 'Server'),
(23, 7, 'Chloe', 'Baker', 21, 'chloe.baker@example.com', '555-3013', 'Server'),
(24, 7, 'Ethan', 'Harris', 21, 'ethan.harris@example.com', '555-3016', 'Chief'),
(25, 7, 'Alex', 'Cruz', 21, 'alex.cruz@example.com', '555-3014', 'Chief'),
(26, 7, 'Ella', 'Roberts', 21, 'ella.roberts@example.com', '555-3015', 'Cashier'),
(27, 8, 'Tim', 'Adams', 1, 'tim.adams@example.com', '555-4011', 'Manager'),
(28, 8, 'Grace', 'Turner', 27, 'grace.turner@example.com', '555-4012', 'Server'),
(29, 8, 'Jack', 'Hughes', 27, 'jack.hughes@example.com', '555-4013', 'Server'),
(30, 8, 'Sophia', 'Bennett', 27, 'sophia.bennett@example.com', '555-4014', 'Chief');

-- Orders
INSERT INTO `Orders` (`order_id`, `customer_id`, `driver_id`, `restaurant_location_id`, `restaurant_id`, `order_time`, `customer_address_id`, `order_status`, `ETA`, `price`) VALUES
(1, 1, 1, 1, 1, '2023-04-13 10:00:00', 1, 'Delivered', 30, 25.00),
(2, 2, 2, 2, 2, '2023-04-13 10:30:00', 2, 'In Delivery', 20, 19.99),
(3, 3, 3, 3, 3, '2023-04-13 11:00:00', 3, 'Waiting For Pickup', 25, 30.50),
(4, 4, 4, 4, 4, '2023-04-13 11:30:00', 4, 'Received', 35, 18.00),
(5, 5, 5, 5, 5, '2023-04-13 12:00:00', 5, 'Delivered', 45, 22.50),
(6, 6, 1, 6, 6, '2023-04-13 12:30:00', 6, 'Canceled', NULL, 16.00),
(7, 7, 2, 7, 7, '2023-04-13 13:00:00', 7, 'Delivered', 40, 24.99),
(8, 8, 3, 8, 8, '2023-04-13 13:30:00', 8, 'In Delivery', 30, 28.00),
(9, 9, 4, 9, 9, '2023-04-13 14:00:00', 9, 'Waiting For Pickup', 20, 20.50),
(10, 10, 5, 10, 10, '2023-04-13 14:30:00', 10, 'Received', 25, 33.00),
(11, 11, 1, 1, 1, '2023-04-13 15:00:00', 11, 'Delivered', 30, 26.50),
(12, 12, 2, 2, 2, '2023-04-13 15:30:00', 12, 'In Delivery', 20, 18.99),
(13, 13, 3, 3, 3, '2023-04-13 16:00:00', 13, 'Waiting For Pickup', 25, 29.50),
(14, 14, 4, 4, 4, '2023-04-13 16:30:00', 14, 'Received', 35, 19.00),
(15, 15, 5, 5, 5, '2023-04-13 17:00:00', 15, 'Delivered', 45, 23.50),
(16, 16, 1, 6, 6, '2023-04-13 17:30:00', 16, 'Canceled', NULL, 17.00),
(17, 17, 2, 7, 7, '2023-04-13 18:00:00', 17, 'Delivered', 40, 25.99),
(18, 18, 3, 8, 8, '2023-04-13 18:30:00', 18, 'In Delivery', 30, 29.00),
(19, 19, 4, 9, 9, '2023-04-13 19:00:00', 19, 'Waiting For Pickup', 20, 21.50),
(20, 20, 5, 10, 10, '2023-04-13 19:30:00', 20, 'Received', 25, 34.00);

-- Payments
INSERT INTO `Payments` (`payment_id`, `order_id`, `card_id`, `price`) VALUES
(1, 1, 1, 15.99),
(2, 2, 2, 8.99),
(3, 3, 3, 12.99),
(4, 4, 4, 5.99),
(5, 5, 5, 9.99),
(6, 6, 6, 14.99),
(7, 7, 7, 7.99),
(8, 8, 8, 11.99),
(9, 9, 9, 4.99),
(10, 10, 10, 10.99),
(11, 11, 11, 19.99),
(12, 12, 12, 6.99),
(13, 13, 13, 15.99),
(14, 14, 14, 8.99),
(15, 15, 15, 12.99),
(16, 16, 16, 5.99),
(17, 17, 17, 9.99),
(18, 18, 18, 14.99),
(19, 19, 19, 8.29),
(20, 20, 20, 7.99);


-- Order_Items
INSERT INTO `Order_Items` (`order_item_id`, `order_id`, `food_id`, `quantity`, `special_instructions`) VALUES
(1, 1, 1, 1, NULL),
(2, 1, 2, 1, 'Extra cheese'),
(3, 2, 3, 2, 'No onions'),
(4, 2, 4, 1, NULL),
(5, 3, 5, 1, 'Spicy'),
(6, 3, 6, 1, NULL),
(7, 4, 7, 1, 'No lettuce'),
(8, 4, 8, 1, NULL),
(9, 5, 9, 1, 'Extra mayo'),
(10, 5, 10, 1, NULL),
(11, 6, 11, 1, 'Extra sauce'),
(12, 6, 12, 1, 'Extra mushrooms'),
(13, 7, 13, 1, 'No peppers'),
(14, 7, 14, 1, 'Extra chicken'),
(15, 8, 15, 2, 'No pineapple'),
(16, 8, 16, 1, 'Extra bacon'),
(17, 9, 17, 1, 'No onion'),
(18, 9, 18, 1, 'Extra lettuce'),
(19, 10, 19, 1, 'Extra tomato'),
(20, 10, 20, 1, 'No tartar sauce');
