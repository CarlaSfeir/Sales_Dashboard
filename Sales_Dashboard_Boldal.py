import pandas as pd
import plotly.express as px
import streamlit as st
#from calendar import month_name


st.set_page_config(
    page_title="Sales Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
)

# ---- READ CSV ----
@st.cache(allow_output_mutation=True)
def get_data_from_excel():
    df = pd.read_excel("C:\\Users\\Christian\\Desktop\\Sales Report 2021 - final.xlsx")
    df["hour"] = pd.to_datetime((df["Time"]).astype(str)).dt.hour
    return df

df = get_data_from_excel()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here")
year_selected = st.sidebar.radio("Select a Year",pd.unique(df["Year"]))

date_selection = st.sidebar.select_slider('Select a Month',sorted(df['Month']))


product = st.sidebar.selectbox(
    "Select the Product Category",pd.unique(df["ItemGroup"])
)

type_of_data = st.sidebar.selectbox("Select the Customer Type", pd.unique(df['CATEGORY1']))

state = st.sidebar.selectbox(
    "Select the State",pd.unique(df["STATE"])
)


city = st.sidebar.selectbox(
    "Select the City",pd.unique(df["City"])
)

# Link filters to data
df_selection = df.query(
    "Year == @year_selected & Month == @date_selection & ItemGroup == @product & CATEGORY1 == @type_of_data & STATE == @state & City == @city"
)


# ---- MAINPAGE ----
st.markdown('''
# :bar_chart: Real-Time Sales Dashboard
''')

#if (len(city) > 0) and (len(customerType) > 0) and (len(productLine) > 0):
#    df_selection = df.query("City == @city & Customer_type == @customerType")

 # KPIs
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


st.markdown("""---""")

# Pie Chart For Gender
pie_sales = px.pie(
    df,
    values="GrossSales$",
    names="Quarter",
    title="<b>Gross Sales by Quarter</b>",
    color="Quarter",
    color_discrete_map={
        'Q1': 'royalblue',
        'Q2': 'darkblue',
        "Q3": "lightblue",
        "Q4": "darkcyan"
    },
    labels={
        "Quarter": "Quarter",
        "GrossSales$": "Gross Sales"
    },
    template="plotly_white")
#st.write(pie_sales)

 # Bar Chart for Customer Type
df_item = df.groupby(['ItemGroup','Month']).sum().reset_index()
bar_item = px.bar(
    df_item,
    x="Month",
    y="GROSSROFIT$",
    title="<b>Monthly Gross Profit by Product Category</b>",
    color="ItemGroup",
    color_discrete_map={
        'ADVPROM': 'royalblue',
        'CONSUM': 'darkblue',
        "DELIVERY": "lightblue",
        "GOODS": "darkcyan"
        },
    template="plotly_white",
    barmode="group",
    labels={
        "Month": "Month",
        "ItemGroup": "Product Category"
        },
    )
bar_item.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
    )

#st.write(bar_item)

# Sales Customer Category
#df_cust = df.groupby(['Payment', 'CATEGORY1','GrossSales$']).sum().reset_index()
#sales_cust = px.bar(
#    df_cust,
#    x="CATEGORY1",
#    y="GrossSales$",
#    title="<b>Sales by Customer Category per Payment Type</b>",
#    color="Payment",
#    color_discrete_map={
#        'Cash': 'royalblue',
#        'Credit card': 'darkblue'
#    },
#    template="plotly_white",
#    barmode="group",
#    facet_col="CATEGORY1",
#    labels={
#        "CATEGORY1": "Customer Category",
#        "GrossSales$": "Gross Sales",
#    },
#)
#sales_cust.update_layout(
#    plot_bgcolor="rgba(0,0,0,0)",
#    xaxis=(dict(showgrid=False)),
#)

#st.write(sales_cust)

c1, c2 = st.columns(2)
c1.plotly_chart(pie_sales, use_container_width=True)
c2.plotly_chart(bar_item, use_container_width=True)


# Gross Profit per state
df_state = df.groupby(['Payment', 'STATE']).sum().reset_index()
sales_state = px.bar(
    df_state,
    x="STATE",
    y="GROSSROFIT$",
    title="<b>Gross Profit per State</b>",
    labels={
        "STATE": "State",
        "GROSSROFIT$": "Gross Profit"
    },
    color="Payment",
    color_discrete_map={
        'Cash': 'royalblue',
        'Credit card': 'darkblue'
    },
    barmode="group",
    template="plotly_white",
)
sales_state.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
)

#st.write(sales_state)

# Line Chart
#df["Total_Discount"] = df["DiscountOfGoodsSold$"] + df["DiscountOfFreeSoldGoods$"]

#df_hour = df.groupby(["Time", "GrossSales$", "Total_Discount"]).sum().reset_index()
#sales_hour = px.line(
#    df_hour,
#    x="Time",
#    y="GrossSales$", "Total_Discount",
#    title="<b>Gross Sales vs. Total Discount per Hour</b>",
#    color="GrossSales$", "Total_Discount",
#    color_discrete_map={
#        'GrossSales$': 'royalblue',
#        'Total_Discount': 'darkblue'
#    },
#    template="plotly_white"
#)
#sales_hour.update_traces(hoverinfo='text+name', mode='lines+markers')
#sales_hour.update_layout(
#    plot_bgcolor="rgba(0,0,0,0)",
#    xaxis=(dict(showgrid=False)),
#    yaxis=(dict(showgrid=False)),
#)

#line_chart = df_hour(columns = ["GrossSales$", "Total_Discount"])
#plot_hour = st.line_chart(df_hour)
#st.write(line_chart)





#c1, c2 = st.columns(2)
#c1.plotly_chart(sales_state, use_container_width=True)
#c2.plotly_chart(plot_hour, use_container_width=True)

#df_sales_cost = df.groupby(['GrossSales$', 'TotalSalesCost$', "Month"]).sum().reset_index()
#chart_data = df_sales_cost("Month", columns["GrossSales$", "TotalSalesCost$"])
#line_sales_cost = st.linechart(df_sales_cost)
#st.write(line_sales_cost)

#df_sales_cost = df.melt('Month', var_name='name', value_name='value')
#st.write(df)

#chart = alt.Chart(df).mark_line().encode(
#  x=alt.X('Duration:N'),
#  y=alt.Y('value:Q'),
#  color=alt.Color("name:N")
#).properties(title="Hello World")
#st.altair_chart(chart, use_container_width=True)

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
    color_discrete_sequence=["#4169e1"] * len(sales_by_customer_category),
    template="plotly_white",
)
fig_col3.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

#st.write(fig_col3)

c3, c4 = st.columns(2)
c3.plotly_chart(sales_state, use_container_width=True)
c4.plotly_chart(fig_col3, use_container_width=True)


#######################################################
#######################################################

