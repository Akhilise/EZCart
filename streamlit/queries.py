# SQL query to insert customer records
INSERT_CUSTOMERS = '''
    INSERT INTO customers (
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix,
        customer_city,
        customer_state
    )
    VALUES (%s,%s,%s,%s,%s)
'''

INSERT_PRODUCT_CATEGORY_TRASLATION = '''
    INSERT INTO product_category_translation(
        product_category_name,
        product_category_name_english
    )
    VALUES (%s,%s)
'''

INSERT_PRODUCTS = """
    INSERT INTO products (
        product_id,
        product_category_name,
        product_name_length,
        product_description_length,
        product_photos_qty,
        product_weight_g,
        product_length_cm,
        product_height_cm,
        product_width_cm
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

INSERT_SELLER = """
    INSERT INTO sellers(
        seller_id ,
        seller_zip_code_prefix ,
        seller_city,
        seller_state
    )
     VALUES (%s, %s, %s, %s)
"""

INSERT_ORDERS = """
    INSERT INTO orders(
       order_id ,
       customer_id,
       order_status,
       order_purchase_timestamp ,
       order_approved_at ,
       order_delivered_carrier_date ,
       order_delivered_customer_date ,
       order_estimated_delivery_date
    
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""