
import pandas as pd

# Read cleaned customer CSV
customer_df = pd.read_csv(
    "./data/cleaned/customers.csv",
    dtype={"customer_zip_code_prefix": "Int64"}
)

# Read cleaned category translation CSV
category_translation_df = pd.read_csv(
    "./data/cleaned/category_translation.csv"
)

# Read cleaned products CSV
products_df = pd.read_csv(
    "./data/cleaned/products.csv"
)

# Read cleaned sellers CSV
sellers_df = pd.read_csv(
    "./data/cleaned/sellers.csv"
)

# Read cleaned orders CSV
orders_df = pd.read_csv(
    "./data/cleaned/orders.csv"
)


# Handle missing and unmatched product categories
valid_categories = category_translation_df[
    "product_category_name"
].dropna()

products_df["product_category_name"] = products_df[
    "product_category_name"
].where(
    products_df["product_category_name"].isin(valid_categories),
    None
)

# Convert missing values to None for MySQL
customer_df = customer_df.astype(object).where(
    pd.notna(customer_df), None
)

category_translation_df = (
    category_translation_df.astype(object)
    .where(pd.notna(category_translation_df), None)
)

products_df = products_df.astype(object).where(
    pd.notna(products_df), None
)

sellers_df = sellers_df.astype(object).where(
    pd.notna(sellers_df), None
)

orders_df = orders_df.astype(object).where(
    pd.notna(orders_df), None
)


# Prepare customer records
CUSTOMER_DATA = list(
    customer_df[
        [
            "customer_id",
            "customer_unique_id",
            "customer_zip_code_prefix",
            "customer_city",
            "customer_state"
        ]
    ].itertuples(index=False, name=None)
)

# Prepare category translation records
CATEGORY_TRANSLATION = list(
    category_translation_df[
        [
            "product_category_name",
            "product_category_name_english"
        ]
    ].itertuples(index=False, name=None)
)

# Prepare product records
PRODUCTS_DATA = list(
    products_df[
        [
            "product_id",
            "product_category_name",
            "product_name_length",
            "product_description_length",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm"
        ]
    ].itertuples(index=False, name=None)
)

# Prepare seller records
SELLERS_DATA = list(
    sellers_df[
        [
            "seller_id",
            "seller_zip_code_prefix",
            "seller_city",
            "seller_state"
        ]
    ].itertuples(index=False ,name=None)
)

# Prepare orders records
ORDERS_DATA = list(
    orders_df[
        [
           "order_id",
           "customer_id",
           "order_status",
           "order_purchase_timestamp" ,
           "order_approved_at",
           "order_delivered_carrier_date",
           "order_delivered_customer_date",
           "order_estimated_delivery_date"
        ]
    ].itertuples(index=False ,name=None)
)
