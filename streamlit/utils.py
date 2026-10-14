import pandas as pd

# Read cleaned customer CSV
customer_df = pd.read_csv(
    "./data/cleaned/customers.csv",
    dtype={"customer_zip_code_prifix": "Int64"}
)
category_translation_df = pd.read_csv(
    "./data/cleaned/category_translation.csv",
)
products_df = pd.read_csv(
    "./data/cleaned/products.csv",
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

CATEGORY_TRANSLATION =  list(
        category_translation_df[
            [
               "product_category_name",
               "product_category_name_english"
            ]
        ].itertuples(index=False, name='Unknown')
    )

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

      