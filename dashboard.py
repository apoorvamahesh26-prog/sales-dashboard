import streamlit as st
import pandas as pd
import plotly.express as px

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Sales & Revenue Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---- TITLE ----
st.title("📊 Sales & Revenue Analysis Dashboard")
st.markdown("---")

# ---- LOAD DATA ----
@st.cache_data
def load_data():
    df = pd.DataFrame({
        "Date": pd.to_datetime([
            "2026-01-05","2026-01-12","2026-01-18",
            "2026-02-03","2026-02-14","2026-02-22",
            "2026-03-05","2026-03-15","2026-03-28",
            "2026-04-10","2026-04-18","2026-04-25",
            "2026-05-08","2026-05-16","2026-05-24",
            "2026-06-02","2026-06-10","2026-06-18"
        ]),
        "Product": [
            "Samsung Galaxy A55","Nike Air Max","Levis Jeans",
            "Sony Headphones","Nescafe Gold","Apple iPad",
            "Puma Sneakers","HM Chinos","Bournvita 1kg",
            "Samsung Galaxy A55","Nike Air Max","Sony Headphones",
            "Levis Jeans","Apple iPad","Nescafe Gold",
            "Puma Sneakers","HM Chinos","Bournvita 1kg"
        ],
        "Category": [
            "Electronics","Sports","Clothing",
            "Electronics","Food & Bev","Electronics",
            "Sports","Clothing","Food & Bev",
            "Electronics","Sports","Electronics",
            "Clothing","Electronics","Food & Bev",
            "Sports","Clothing","Food & Bev"
        ],
        "Region": [
            "North","South","East","West","North","South",
            "East","West","North","South","West","North",
            "South","East","West","North","South","East"
        ],
        "Units_Sold": [
            45,30,60,25,120,15,40,75,200,
            55,35,20,80,18,150,50,90,180
        ],
        "Unit_Price": [
            16000,5500,2500,18000,500,35000,
            4000,1800,450,16000,5500,18000,
            2500,35000,500,4000,1800,450
        ],
        "Revenue": [
            720000,165000,150000,450000,60000,525000,
            160000,135000,90000,880000,192500,360000,
            200000,630000,75000,200000,162000,81000
        ]
    })
    return df

df = load_data()

# ---- FILTERS (SLICERS) ----
st.sidebar.header("🎛️ Filters")

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

# Apply filters
df_filtered = df[
    (df["Category"].isin(category)) &
    (df["Region"].isin(region))
]

# ---- KPI CARDS ----
st.subheader("📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Total Revenue",
        f"₹{df_filtered['Revenue'].sum():,.0f}")

with col2:
    st.metric("🛒 Total Units Sold",
        f"{df_filtered['Units_Sold'].sum():,}")

with col3:
    st.metric("📦 Avg Order Value",
        f"₹{df_filtered['Revenue'].mean():,.0f}")

with col4:
    st.metric("🏷️ Total Products",
        f"{df_filtered['Product'].nunique()}")

st.markdown("---")

# ---- CHARTS ----
col5, col6 = st.columns(2)

with col5:
    st.subheader("📊 Revenue by Category")
    fig1 = px.pie(
        df_filtered, values="Revenue",
        names="Category", hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(fig1, use_container_width=True)

with col6:
    st.subheader("🗺️ Revenue by Region")
    fig2 = px.bar(
        df_filtered.groupby("Region")["Revenue"].sum().reset_index(),
        x="Region", y="Revenue",
        color="Region",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---- REVENUE TREND ----
st.subheader("📈 Revenue Trend Over Time")
df_trend = df_filtered.groupby("Date")["Revenue"].sum().reset_index()
fig3 = px.line(
    df_trend, x="Date", y="Revenue",
    markers=True, line_shape="spline",
    color_discrete_sequence=["#4f8ef7"]
)
st.plotly_chart(fig3, use_container_width=True)

# ---- TOP PRODUCTS ----
st.subheader("🏆 Top Performing Products")
top_products = df_filtered.groupby("Product")["Revenue"].sum()\
    .reset_index().sort_values("Revenue", ascending=False)
fig4 = px.bar(
    top_products, x="Revenue", y="Product",
    orientation="h",
    color="Revenue",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig4, use_container_width=True)

# ---- DATA TABLE ----
st.subheader("📋 Raw Data")
st.dataframe(df_filtered, use_container_width=True)

st.markdown("---")
st.caption("Sales & Revenue Dashboard | Thiranex Data Analytics Internship")