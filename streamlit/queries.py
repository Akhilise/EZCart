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