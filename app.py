import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🛒 E-Commerce Sales Dashboard")
st.write("Interactive Sales Analysis using Pandas, Plotly and Streamlit")

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

df = pd.read_csv("Sample - Superstore1.csv")

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------

st.sidebar.header("🔍 Filters")

categories = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].dropna().unique()),
    default=sorted(df["Category"].dropna().unique())
)

regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

segments = st.sidebar.multiselect(
    "Select Customer Segment",
    options=sorted(df["Segment"].dropna().unique()),
    default=sorted(df["Segment"].dropna().unique())
)

# --------------------------------------------------
# Apply Filters
# --------------------------------------------------

filtered_df = df[
    (df["Category"].isin(categories)) &
    (df["Region"].isin(regions)) &
    (df["Segment"].isin(segments))
]

# --------------------------------------------------
# Check Filtered Data
# --------------------------------------------------

if filtered_df.empty:

    st.warning("No data available for the selected filters.")

else:

    # --------------------------------------------------
    # KPI Calculations
    # --------------------------------------------------

    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    total_orders = filtered_df["Order ID"].nunique()
    total_customers = filtered_df["Customer ID"].nunique()

    # --------------------------------------------------
    # KPI Cards
    # --------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Total Sales",
        f"${total_sales:,.2f}"
    )

    col2.metric(
        "📈 Total Profit",
        f"${total_profit:,.2f}"
    )

    col3.metric(
        "🛒 Total Orders",
        f"{total_orders:,}"
    )

    col4.metric(
        "👥 Total Customers",
        f"{total_customers:,}"
    )

    st.divider()

    # --------------------------------------------------
    # Sales by Category
    # --------------------------------------------------

    st.subheader("📊 Sales by Category")

    category_sales = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig1 = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        title="Sales by Category",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # --------------------------------------------------
    # Sales by Region
    # --------------------------------------------------

    st.subheader("🌍 Sales by Region")

    region_sales = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        region_sales,
        names="Region",
        values="Sales",
        title="Sales Distribution by Region"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # --------------------------------------------------
    # Profit by Category
    # --------------------------------------------------

    st.subheader("💵 Profit by Category")

    category_profit = (
        filtered_df
        .groupby("Category")["Profit"]
        .sum()
        .reset_index()
    )

    fig3 = px.bar(
        category_profit,
        x="Category",
        y="Profit",
        title="Profit by Category",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # --------------------------------------------------
    # Sales by Customer Segment
    # --------------------------------------------------

    st.subheader("👥 Sales by Customer Segment")

    segment_sales = (
        filtered_df
        .groupby("Segment")["Sales"]
        .sum()
        .reset_index()
    )

    fig4 = px.bar(
        segment_sales,
        x="Segment",
        y="Sales",
        title="Sales by Customer Segment",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    # --------------------------------------------------
    # Top 10 Products
    # --------------------------------------------------

    st.subheader("🏆 Top 10 Products by Sales")

    product_sales = (
        filtered_df
        .groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig5 = px.bar(
        product_sales.sort_values("Sales"),
        x="Sales",
        y="Product Name",
        orientation="h",
        title="Top 10 Products by Sales",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

    # --------------------------------------------------
    # Dataset Preview
    # --------------------------------------------------

    st.subheader("📋 Filtered Dataset")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )