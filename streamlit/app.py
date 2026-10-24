
import streamlit as st
import pandas as pd

from database import get_connection
from queries import (BUSINESS_OVERVIEW_QUERY, 
                     MONTHLY_REVENUE_QUERY,
                     YEARLY_REVENUE_QUERY,
                     CATEGORY_REVENUE_QUERY,
                     TOP_SELLING_PRODUCTS_QUERY,
                     SALES_BY_LOCATION_QUERY,
                     CUSTOMER_DISTRIBUTION_QUERY,
                     CUSTOMER_SPENDING_QUERY,
                     REPEAT_CUSTOMER_QUERY,
                     TOP_CUSTOMERS_QUERY,
                     SELLER_REVENUE_QUERY,
                     SELLER_RATINGS_QUERY,AVERAGE_DELIVERY_TIME_QUERY)


st.set_page_config(
    page_title="EZCart",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="locked"
)

with st.sidebar:
  st.title("🛒 EZCart")
  st.subheader("E-Commerce Business Overview")
  
  page = st.radio(
      "Overviews",
      [ "Business Overview",
        "Sales Analysis",
        "Customer Analysis",
        "Seller & Product Analysis",
        "Delivery Analysis",
        "Customer Experience",]
  )

connection = get_connection()

try:
    if page =="Business Overview":
     st.title("Business Overview")

     df = pd.read_sql(BUSINESS_OVERVIEW_QUERY, connection)

     metrics = df.loc[0]
     col1, col2, col3 = st.columns(3)

     col1.metric("Total Revenue", f"{metrics['total_revenue']:,.2f}")
     col2.metric("Total Orders", f"{metrics['total_orders']:,}")
     col3.metric("Total Customers", f"{metrics['total_customers']:,}")

     col4, col5, col6 = st.columns(3)

     col4.metric("Total Sellers", f"{metrics['total_sellers']:,}")
     col5.metric("Average Order Value", f"{metrics['average_order_value']:,.2f}")
     col6.metric("Average Review Score", f"{metrics['average_review_score']:,.2f}/5")
     
    elif page =="Sales Analysis":
        st.header("Sales Analysis")
          
        revenue_selector = st.radio(
                "Select Revenue Period",
                ['Monthly', 'Yearly'],
                horizontal=True
            )
        if revenue_selector == 'Monthly':
                df_revenue = pd.read_sql(MONTHLY_REVENUE_QUERY, connection)
                x_column = "order_month"
                x_label = "Monthly Orders"
                chart_title = "Monthly Revenue Trend"
        else:
                df_revenue = pd.read_sql(YEARLY_REVENUE_QUERY, connection)
                x_column = "order_year"
                x_label = "Yearly Orders"
                chart_title = "Yearly Revenue Trend"
        
        st.subheader(chart_title)
        
        st.line_chart(
                df_revenue,
                x=x_column,
                y="total_revenue",
                x_label=x_label,
                y_label="Total Revenue"
            )
        
        st.dataframe(df_revenue, use_container_width=True)
        
        st.divider()
        st.subheader("Top 10 Product Categories by Revenue")
        
        df_category = pd.read_sql(CATEGORY_REVENUE_QUERY, connection)
        
        st.bar_chart(
                df_category,
                x="product_category",
                y="category_revenue",
                x_label="Product Category",
                y_label="Revenue",
                horizontal=True
            )
        
        st.dataframe(df_category, use_container_width=True)
        
        st.divider()
        st.header("Top 10 Selling Products")
        
        df_products = pd.read_sql(
                TOP_SELLING_PRODUCTS_QUERY,
                connection
            )
        
        st.bar_chart(
                df_products,
                x="product_name",
                y="product_revenue",
                x_label="Product Name",
                y_label="Product Revenue",
                horizontal=True
            )
        
        st.dataframe(
                df_products,
                use_container_width=True
            )
        
        st.divider()
        st.subheader("Sales by location")
        
        df_location = pd.read_sql(SALES_BY_LOCATION_QUERY, connection)
        
        st.bar_chart(
                df_location,
                x="customer_state",
                y="total_revenue",
                x_label="Customer State",
                y_label="Total Revenue",
                horizontal=True
            )
        
        st.dataframe(df_location, use_container_width=True)

    elif page == "Customer Analysis":
        st.header("Customer Analysis")
        df_customer = pd.read_sql(CUSTOMER_DISTRIBUTION_QUERY,connection)
        
        st.subheader("Customer Distribution by State")

        st.bar_chart(
            df_customer,
            x="customer_state",
            y="total_customers",
            x_label="Customer State",
            y_label="Total Customers",
            horizontal=True
        )

        st.dataframe(
            df_customer,
            use_container_width=True
        )


        st.divider()
        st.subheader("Customer Spending")

        df_spending = pd.read_sql(
            CUSTOMER_SPENDING_QUERY,
            connection
        )

        st.bar_chart(
            df_spending.head(10),
            x="customer_unique_id",
            y="total_spending",
            x_label="Customer ID",
            y_label="Total Spending",
            horizontal=True
        )

        st.divider()
        st.subheader("Repeat vs New Customers")

        df_repeat = pd.read_sql(
            REPEAT_CUSTOMER_QUERY,
            connection
        )

        st.bar_chart(
            df_repeat,
            x="customer_type",
            y="total_customers",
            x_label="Customer Type",
            y_label="Total Customers"
        )

        st.dataframe(df_repeat, use_container_width=True)

        st.divider()
        st.subheader("Top 10 Customers by Spending")

        df_top_customers = pd.read_sql(
            TOP_CUSTOMERS_QUERY,
            connection
        )

        st.bar_chart(
            df_top_customers,
            x="customer_unique_id",
            y="total_spending",
            x_label="Customer ID",
            y_label="Total Spending",
            horizontal=True
        )

        st.dataframe(
            df_top_customers,
            use_container_width=True
        )



    elif page == "Seller & Product Analysis":
        st.header("Seller & Product Analysis")
        st.subheader("Top Sellers by Revenue")

        df_sellers = pd.read_sql(SELLER_REVENUE_QUERY,connection)

        st.bar_chart(
        df_sellers,
        x="seller_id",
        y="seller_revenue",
        x_label="Seller ID",
        y_label="Seller Revenue",
        horizontal=True
        )

        st.dataframe(df_sellers,use_container_width=True)
        
        st.subheader("Top Sellers by Rating")
        df_sellers_rating = pd.read_sql(SELLER_RATINGS_QUERY,connection)
        
        st.bar_chart(
        df_sellers_rating,
        x="seller_id",
        y="average_rating",
        x_label="Seller ID",
        y_label="Seller Rating",
        horizontal=True
        )
        
        st.dataframe(df_sellers_rating,use_container_width=True)
        
        st.divider()
        st.subheader("Product Category Performance")

        df_category = pd.read_sql(CATEGORY_REVENUE_QUERY,connection)

        st.bar_chart(
        df_category,
        x="product_category",
        y="category_revenue",
        x_label="Product Category",
        y_label="Category Revenue",
        horizontal=True
        )

        st.dataframe(df_category,use_container_width=True)
        

    elif page == "Delivery Analysis":
        st.header("Delivery Analysis")
        
        st.subheader("Average Delivery Time")

        df_delivery = pd.read_sql(AVERAGE_DELIVERY_TIME_QUERY,connection)

        average_days = df_delivery.loc[0, "average_delivery_days"]

        st.metric(f"{average_days:.2f} days")

    elif page == "Customer Experience":
        st.header("Customer Experience")


except Exception as e:
    st.error(f"An error occurred: {e}")

finally:
    connection.close()
