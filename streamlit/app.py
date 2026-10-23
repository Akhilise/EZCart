import streamlit as st
import pandas as pd

from database import get_connection
from queries import (BUSINESS_OVERVIEW_QUERY, 
                     MONTHLY_REVENUE_QUERY,
                     YEARLY_REVENUE_QUERY,
                    CATEGORY_REVENUE_QUERY,
                    TOP_SELLING_PRODUCTS_QUERY)


st.set_page_config(
    page_title = 'EZCart',
    page_icon="🛒",
    layout='wide'
)

st.title("🛒 EZCart")
st.subheader("E-Commerce Business Overview")

connection = get_connection()

try:
    df= pd.read_sql(BUSINESS_OVERVIEW_QUERY,connection)
    
    metrics = df.loc[0]
    col1,col2,col3  = st.columns(3)
    
    col1.metric("Total Revenue" , f"{metrics['total_revenue']:,.2f}")
    col2.metric("Total Orders" , f"{metrics['total_orders']:,}")
    col3.metric("Total Customers" , f"{metrics['total_customers']:,}")
    
    col4,col5,col6 = st.columns(3)
    
    col4.metric("Total Sellers" , f"{metrics['total_sellers']:,}")
    col5.metric("Average Order Value" , f"{metrics['average_order_value']:,.2f}")
    col6.metric("Average Review Score" , f"{metrics['average_review_score']:,.2f}/5")
    
    st.divider()
    st.header("Sales Analysis")
    
    revenue_selector = st.radio(
        "Select Revenue Period",
        ['Monthly','Yearly'],
        horizontal=True
    )
    
    if revenue_selector == 'Monthly':
            df_revenue = pd.read_sql(
                MONTHLY_REVENUE_QUERY, connection
            )
            x_column = "order_month"
            x_label = "Monthly Orders"
            chart_title = "Monthly Revenue Trend"
    else:
            df_revenue = pd.read_sql(
                YEARLY_REVENUE_QUERY, connection
            )
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
    
    df_category = pd.read_sql(
        CATEGORY_REVENUE_QUERY, connection
    )
    
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

    
  

    
    
except Exception as e:
    st.error(f"An error occurred: {e}")
    
finally:
    connection.close()

    

