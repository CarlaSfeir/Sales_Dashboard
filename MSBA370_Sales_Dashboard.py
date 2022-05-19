import pandas as pd
import streamlit as st
import plotly.express as px

#import time  # to simulate a real time data, time loop
import numpy as np  # np mean, np random



# dashboard setup
st.set_page_config(
    page_title="Real-Time Sales Report Dashboard",
    page_icon="✅",
    layout="wide",
)


# read excel file
@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_excel("C:\\Users\\Christian\\Desktop\\Sales Report 2021 - final.xlsx")


df = get_data()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here")
year_selected = st.sidebar.radio("Year",pd.unique(df["Year"]))

product = st.sidebar.selectbox(
    "Select the Product Category",pd.unique(df["ItemGroup"])
)

type_of_data = st.sidebar.selectbox("Select the Customer Type", pd.unique(df['CATEGORY1']))
#customer_type = st.sidebar.multiselect(
#    "Select the Customer Type:",
#    options=df["CATEGORY1"].unique(),
#    default=df["CATEGORY1"].unique(),
#)


state = st.sidebar.selectbox(
    "Select the State",pd.unique(df["STATE"])
)


city = st.sidebar.selectbox(
    "Select the City",pd.unique(df["City"])
)

#city = st.sidebar.multiselect(
#    "Select the City:",
#    options=df["City"].unique(),
#    default=df["City"].unique()
#)




#df_selection = df.query(
#    "City == @city & Customer_type ==@customer_type & Gender == @gender"
#)





# dashboard title
st.title(":bar_chart: Real-Time Sales Report Dashboard")

# top-level filters
#customer_type = st.selectbox("Select the Customer Type", pd.unique(df["CATEGORY1"]))

# dataframe filter
#df = df[df["ItemGroup"] == category_filter]

#st.table(df["GrossSales$"].style.format("{:.2}"))
#df["some_column"] = df["some_column"].astype(int)
#st.table(df["GrossSales$"].style.format(precision=0))
#st.table(df["GrossSales$"].style.format('{:7,.1f}'))
#st.dataframe(df.style.format(subset=['GrossSales$', 'CostOfGoodsSold$'], formatter="{:.2f}"))

# TOP KPI's
total_qty = int(df["TotalQtySold"].sum())
total_gross_sales = round(((df["GrossSales$"]/1000000).sum()),2)
total_discount = round(((((df["DiscountOfGoodsSold$"]+df['DiscountOfFreeSoldGoods$'])/1000000).sum())),2)
total_cost = round(((df["TotalSalesCost$"]/1000000).sum()),2)
gp_perc = round(((df["GROSSROFIT$"].sum())/(df["InvoicedSales$"].sum()))*100,1)

first_column, second_column, third_column, fourth_column, fifth_column = st.columns(5)
with first_column:
    st.subheader("Total Quantity Sold")
    st.subheader(f"{total_qty:,}")
with second_column:
    st.subheader("Total Gross Sales")
    st.subheader(f"US$ {total_gross_sales:,} M")
with third_column:
    st.subheader("Total Discount")
    st.subheader(f"US$ {total_discount} M")
with fourth_column:
    st.subheader("Total Cost")
    st.subheader(f"US$ {total_cost} M")
with fifth_column:
    st.subheader("Gross Profit")
    st.subheader(f"% {gp_perc}")




# create three columns
#kpi1 = st.columns(1)

# fill in those three columns with respective metrics or KPIs
#kpi1.metric(
#    label="Total Quantity Sold",
#    value=f"${int(TotalQtySold)}",
#    delta=f"${int(TotalQtySold)}" - 10,
#)

#kpi2.metric(
#    label="Gross Sales in $",
#    value=f"${int('GrossSales$')}",
#    delta=-10 + 'GrossSales$',
#)

#kpi3.metric(
#    label="Total Discount",
#    value=f"$ {round(balance,2)} ",
#    delta=-round(balance / count_married) * 100,
#)

#chart_qty = df.drop(['DocumentNo', "InvoiceNo", "FinancialDate", "Year", "City", "STATE", "COUNTY", "CustomerCode", "CustomerName", "CATEGORY1", "CHAIN1", "SREPCODE", "Salesrep", "WarehouseId", "BrandCode", "ProductCode", "ItemGroup", "QtySold", "FreeQtySold", "GrossSales$", "GrossSalesLBP", "DiscountOfGoodsSold$", "DiscountOfFreeSoldGoods$", "InvoicedSales$", "CostOfGoodsSold$", "RATE", "CostOfFreeSoldGoods$", "CostOfFreeSoldGoods100$", "CostOfAdvProm$", "CostOfConsum$", "TotalSalesCost$", "GROSSROFIT$"], axis=1)

chart_quantity = df.groupby('Month')[['TotalQtySold']].sum()
#st.write(df)
#st.bar_chart(df)
chart_salescost = df.groupby('Month')[['TotalSalesCost$', "GrossSales$"]].sum()


# create two columns for charts
fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("### Total Quantity Sold")
    fig = st.bar_chart(chart_quantity)
#    st.write(fig)



#with fig_col2:
#    st.markdown("### Gross Sales vs. Cost by Month")
#    fig_col2 = st.line_chart(
#        data=chart_salescost, y=["GrossSales$"], x="Month"
#    )
#    st.write(fig_col2)
   

df["TotalDiscount$"] = (df["DiscountOfGoodsSold$"]+df['DiscountOfFreeSoldGoods$'])
#chart_grosssales = df.groupby('Month')[['GrossSales$', "TotalDiscount$"]].sum()

#with fig_col2:
#    st.markdown("### Sales vs. Cost per Month")
#    fig2 = px.histogram(data_frame=chart_grosssales, x="Month")
#    st.write(fig2)

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_customer_category = (
    df.groupby(by=["CATEGORY1"]).sum()[["GROSSROFIT$"]].sort_values(by="GROSSROFIT$")
)
fig_col3 = px.bar(
    sales_by_customer_category,
    x="GROSSROFIT$",
    y=sales_by_customer_category.index,
    orientation="h",
    title="<b>Sales by Customer Category</b>",
    color_discrete_sequence=["#b8003a"] * len(sales_by_customer_category),
    template="plotly_white",
)
fig_col3.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

st.write(fig_col3)

