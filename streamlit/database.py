import os
import mysql.connector as mysql
from dotenv import load_dotenv
from mysql.connector import Error
from queries import (INSERT_CUSTOMERS, INSERT_PRODUCT_CATEGORY_TRASLATION,
                     INSERT_PRODUCTS,
                     INSERT_SELLER,
                     INSERT_ORDERS,
                     INSERT_ORDER_ITEMS,
                     INSERT_ORDER_PAYMENT,
                     INSERT_ORDER_REVIEWS,
                     INSERT_GEOLOCATION)
from utils import (CATEGORY_TRANSLATION, 
                   CUSTOMER_DATA, 
                   PRODUCTS_DATA,
                   SELLERS_DATA,
                   ORDERS_DATA,
                   ORDER_ITEMS_DATA,
                   ORDER_PAYMENT_DATA,
                   ORDER_REVIEW_DATA,
                   GEOLOCATION_DATA)

# Load environment variables
load_dotenv()

# Get database credentials
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")


def main():
    connection = None
    cursor = None

    try:
        # Connect to MySQL
        connection = mysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            print("Connected to MySQL database")

        # Create cursor
        cursor = connection.cursor()


        # Keep customer loader unchanged
        def load_customer():
            cursor.executemany(INSERT_CUSTOMERS, CUSTOMER_DATA)
            connection.commit()
            print(f"Inserted {cursor.rowcount} records into customers table")

        # Run this loader last
        #load_customer()

        # Load category translation
        def load_category_translation():
            cursor.executemany(
                INSERT_PRODUCT_CATEGORY_TRASLATION,
                CATEGORY_TRANSLATION
            )
            connection.commit()
            print(
                f"Inserted {cursor.rowcount} records "
                "into category_translation table"
            )

        # Run this loader first
        #load_category_translation()

        def load_products():
            cursor.executemany(
                INSERT_PRODUCTS,
                PRODUCTS_DATA
            )
            connection.commit()
            print(f"Inserted {cursor.rowcount} records into products table")

        # Run only this loader
        #load_products()


        def load_sellers():
            cursor.executemany(
                INSERT_SELLER,
                SELLERS_DATA
            )
            connection.commit()
            print(f"Inserted {cursor.rowcount} records into sellers table")

        # Run only this loader
        #load_sellers()  

        def load_orders():
            cursor.executemany(
                INSERT_ORDERS,
                ORDERS_DATA
                    )
            connection.commit()
            print(f"Inserted {cursor.rowcount} records into orders table")
        
        # Run only this loader
        #load_orders()    

        def load_order_items():
            cursor.executemany(
                INSERT_ORDER_ITEMS,
                ORDER_ITEMS_DATA
            )
            connection.commit()
            print(f"Inserted {cursor.rowcount} records into orders items table")
        
        # Run only this loader
        #load_order_items() 
        
        def load_order_payments():
         cursor.executemany(
             INSERT_ORDER_PAYMENT,
             ORDER_PAYMENT_DATA
            )
         connection.commit()
         print(f"Inserted {cursor.rowcount} records into order_payment table")
         
         
        #load_order_payments()
  
  

        def load_order_reviews():
            cursor.executemany(
                INSERT_ORDER_REVIEWS,
                ORDER_REVIEW_DATA
            )
            connection.commit()
            print(f"Inserted {cursor.rowcount} records into order_reviews table")
        
        
        #load_order_reviews()
    
        def load_geolocation():
            cursor.executemany(
                INSERT_GEOLOCATION,
                GEOLOCATION_DATA
            )
            connection.commit()
            print(f"Inserted {cursor.rowcount} records into geolocation table")
            
        load_geolocation()
        
    except (Error, OSError, ValueError) as e:
        if connection is not None and connection.is_connected():
            connection.rollback()

        print("Something went wrong:", e)

    finally:
        # Close cursor and connection
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


if __name__ == "__main__":
    main()