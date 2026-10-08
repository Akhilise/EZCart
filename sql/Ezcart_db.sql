CREATE DATABASE ezcart;

USE ezcart;

# Creating customer table
CREATE TABLE customers (
customer_id VARCHAR(50) PRIMARY KEY,
customer_unique_id VARCHAR(50),
customer_zip_code_prifix INT,
customer_city VARCHAR(100),
customer_state VARCHAR(10)
);

# Creating Order table
CREATE TABLE orders(
order_id VARCHAR(50) PRIMARY KEY,
customer_id VARCHAR(50) NOT NULL,
order_status VARCHAR(30),
order_purchase_timestamp DATETIME,
order_approved_at DATETIME,
order_delivered_carrier_date DATETIME,
order_delivered_customer_date DATETIME,
order_estimated_delivery_date DATETIME,

FOREIGN KEY(customer_id)
REFERENCES customers(customer_id)
);

#Creating Product Category Translation table
CREATE TABLE product_category_translation (
product_category_name VARCHAR(100) PRIMARY KEY,
product_category_name_english VARCHAR(100)
);

# Creating product table 
CREATE TABLE products (
product_id VARCHAR(50) PRIMARY KEY,
product_category_name VARCHAR(100),
product_name_length INT,
product_description_length INT,
product_photo_qty INT,
product_weight_g INT,
product_length_cm INT,
product_height_cm INT,
product_width_cm INT,

FOREIGN KEY (product_category_name)
REFERENCES product_category_translation(product_category_name)
);

# Creating seller table
CREATE TABLE sellers (
seller_id VARCHAR(50) PRIMARY KEY,
seller_zip_code_prefix INT,
seller_city VARCHAR(100),
seller_state VARCHAR(10)
);

# Creating order item table
CREATE TABLE order_items(
order_id VARCHAR(50) NOT NULL,
order_item_id INT NOT NULL,
product_id VARCHAR(50) NOT NULL,
seller_id VARCHAR(50) NOT NULL,
shipping_limit_date DATETIME,
price DECIMAL(10,2),
freight_value DECIMAL(10,2),

/*order_item_id alone is not unique because it repeats for different orders ,So we use (order_id,order_item_id) this 
uniquely  identifies each item
*/
PRIMARY KEY (order_id,order_item_id),  

FOREIGN KEY (order_id)
REFERENCES orders(order_id),

FOREIGN KEY (product_id)
REFERENCES products(product_id),

FOREIGN KEY (seller_id)
REFERENCES sellers(seller_id)
);

# Creating order_payment table
CREATE TABLE order_payment (
order_id VARCHAR(50) NOT NULL,
payment_sequential INT NOT NULL,
payment_type VARCHAR(30),
payment_installment INT,
payment_value DECIMAL(10,2),

PRIMARY KEY (order_id ,payment_sequential),

FOREIGN KEY (order_id)
REFERENCES orders(order_id)
);

# Creating order_review table

CREATE TABLE order_reviews(
review_id VARCHAR(50) NOT NULL,
order_id VARCHAR(50) NOT NULL,
review_score INT,
review_comment_title TEXT,
review_comment_message TEXT,
review_creation_date DATETIME,
review_answer_timestamp DATETIME,

PRIMARY KEY (review_id,order_id),

FOREIGN KEY (order_id)
REFERENCES orders(order_id)
);

# Creating geolocation table 
CREATE TABLE geolocation(
geolocation_zip_code_prefix INT,
geolocation_lat DECIMAL(11,8),
geolocation_lng DECIMAL(11,8),
geolocation_city VARCHAR(100),
geolocation_state VARCHAR(50)
);

# SHOW ALL TABLE 
SHOW TABLES;




































