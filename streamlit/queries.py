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

INSERT_ORDER_ITEMS = """
    INSERT INTO order_items(
        order_id,
        order_item_id,
        product_id,
        seller_id,
        shipping_limit_date,
        price,
        freight_value
     )
     VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

INSERT_ORDER_PAYMENT= """
    INSERT INTO order_payment(
         order_id,
         payment_sequential,
         payment_type,
         payment_installments,
         payment_value
    ) 
    VALUES(%s, %s, %s, %s, %s)
"""

INSERT_ORDER_REVIEWS = """
    INSERT INTO order_reviews(
        review_id,
        order_id,
        review_score,
        review_comment_title,
        review_comment_message,
        review_creation_date,
        review_answer_timestamp
    )
    VALUES(%s, %s, %s, %s, %s, %s, %s)
"""

INSERT_GEOLOCATION = """
    INSERT INTO geolocation (
        geolocation_zip_code_prefix,
        geolocation_lat,
        geolocation_lng,
        geolocation_city,
        geolocation_state
    )
    VALUES (%s, %s, %s, %s, %s)
"""



BUSINESS_OVERVIEW_QUERY = """
SELECT
    (SELECT ROUND(SUM(price + freight_value), 2)
     FROM order_items) AS total_revenue,

    (SELECT COUNT(DISTINCT order_id)
     FROM orders) AS total_orders,

    (SELECT COUNT(DISTINCT customer_unique_id)
     FROM customers) AS total_customers,

    (SELECT COUNT(DISTINCT seller_id)
     FROM sellers) AS total_sellers,

    (SELECT ROUND(AVG(order_value), 2)
     FROM (
         SELECT order_id, SUM(price + freight_value) AS order_value
         FROM order_items
         GROUP BY order_id
     ) AS order_totals) AS average_order_value,

    (SELECT ROUND(AVG(review_score), 2)
     FROM order_reviews) AS average_review_score;
"""

MONTHLY_REVENUE_QUERY = """
SELECT
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS order_month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS total_revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY order_month
ORDER BY order_month;
"""

YEARLY_REVENUE_QUERY = """
SELECT
    YEAR(o.order_purchase_timestamp) AS order_year,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS total_revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY order_year
ORDER BY order_year;
"""

CATEGORY_REVENUE_QUERY = """
SELECT
    COALESCE(
        pct.product_category_name_english,
        p.product_category_name,
        'Unknown'
    ) AS product_category,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS category_revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN product_category_translation pct
    ON p.product_category_name = pct.product_category_name
GROUP BY product_category
ORDER BY category_revenue DESC
LIMIT 10;
"""


TOP_SELLING_PRODUCTS_QUERY = """
SELECT
    oi.product_id,
    COALESCE(
        pct.product_category_name_english,
        p.product_category_name,
        'Unknown'
    ) AS product_name,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS product_revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN product_category_translation pct
    ON p.product_category_name = pct.product_category_name
GROUP BY
    oi.product_id,
    product_name
ORDER BY product_revenue DESC
LIMIT 10;
"""

SALES_BY_LOCATION_QUERY = """
SELECT 
   c.customer_state,
   ROUND(SUM(price+freight_value),2)AS total_revenue
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.order_status = "delivered"
GROUP BY c.customer_state
ORDER BY total_revenue DESC;
"""

CUSTOMER_DISTRIBUTION_QUERY = """
SELECT
    customer_state,
    COUNT(DISTINCT customer_unique_id) AS total_customers
FROM customers
GROUP BY customer_state
ORDER BY total_customers DESC;
"""

CUSTOMER_SPENDING_QUERY = """
SELECT
    c.customer_unique_id,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS total_spending
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_unique_id
ORDER BY total_spending DESC;
"""

REPEAT_CUSTOMER_QUERY = """
SELECT
    CASE
        WHEN customer_orders > 1 THEN 'Repeat Customer'
        ELSE 'New Customer'
    END AS customer_type,
    COUNT(*) AS total_customers
FROM (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS customer_orders
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
) AS customer_summary
GROUP BY customer_type;
"""


TOP_CUSTOMERS_QUERY = """
SELECT
    c.customer_unique_id,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS total_spending
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_unique_id
ORDER BY total_spending DESC
LIMIT 10;
"""

SELLER_REVENUE_QUERY = """
SELECT
    oi.seller_id,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS seller_revenue
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY oi.seller_id
ORDER BY seller_revenue DESC
LIMIT 10;
"""

SELLER_RATINGS_QUERY = """
SELECT
    oi.seller_id,
    ROUND(AVG(r.review_score), 2) AS average_rating,
    COUNT(r.review_id) AS total_reviews
FROM order_items oi
JOIN order_reviews r
    ON oi.order_id = r.order_id
GROUP BY oi.seller_id
HAVING COUNT(r.review_id) >= 5
ORDER BY average_rating DESC
LIMIT 10;
"""

CATEGORY_REVENUE_QUERY = """
SELECT
    COALESCE(
        pct.product_category_name_english,
        p.product_category_name,
        'Unknown'
    ) AS product_category,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS category_revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN product_category_translation pct
    ON p.product_category_name = pct.product_category_name
GROUP BY product_category
ORDER BY category_revenue DESC
LIMIT 10;
"""

AVERAGE_DELIVERY_TIME_QUERY = """
SELECT
    ROUND(AVG(DATEDIFF(
                order_delivered_customer_date,
                order_purchase_timestamp)),2) AS average_delivery_days
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL;
"""





