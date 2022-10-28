import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide",

                   )


def getDataFromExcel():
    dF = pd.read_excel(
        io='supermarkt_sales.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        nrows=1000,
    )
    dF["hour"] = pd.to_datetime(dF["Time"], format="%H:%M:%S").dt.hour
    return dF


dF = getDataFromExcel()
st.sidebar.header("Select the Filter here")
cityName = st.sidebar.multiselect(label="Select city name here:",
                                  options=dF["City"].unique(),
                                  default=dF["City"].unique()
                                  )

customerType = st.sidebar.multiselect(label="Select customer type here:",
                                      options=dF["Customer_type"].unique(),
                                      default=dF["Customer_type"].unique()
                                      )
gender = st.sidebar.multiselect(label="Select customer gender here:",
                                options=dF["Gender"].unique(),
                                default=dF["Gender"].unique()
                                )
selectionQuery = dF.query("City == @cityName & Customer_type == @customerType & Gender == @gender")

# -------- main Page --------#
st.title(":bar_chart: Sales Dashboard")
st.markdown("---")

totalSum = int(selectionQuery["Total"].sum())
averageRating = round(selectionQuery["Rating"].mean(), 1)
starRating = ":star:" * int(round(averageRating, 0))
averageSaleTransaction = round(selectionQuery["Total"].mean(), 2)

leftCol, middleCol, rightCol = st.columns(3)

with leftCol:
    st.subheader("Total Sum: ")
    st.subheader("US $ " + str('{:,}'.format(totalSum)))
with middleCol:
    st.subheader("Average Rating: ")
    st.subheader(str(averageRating) + " " + str(starRating))
with rightCol:
    st.subheader("Average Sale By transaction: ")
    st.subheader("US $" + str('{:,}'.format(averageSaleTransaction)))

st.markdown("---")

# ----- visual Stuff -----#
salesByProduct = selectionQuery.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")

barChartByProductLine = px.bar(salesByProduct,
                               x="Total",
                               y=salesByProduct.index,
                               orientation='h',
                               title="<b>Sales by Product Line</b>",
                               color_discrete_sequence=["#0083B8"] * len(salesByProduct),
                               template="plotly_white",
                               )
barChartByProductLine.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                                    xaxis=(dict(showgrid=False)))

salesByTime = selectionQuery.groupby(by=["hour"]).sum()[["Total"]]
barChartByHour = px.bar(salesByTime,
                        x=salesByTime.index,
                        y="Total",
                        title="<b>Sales by hour</b>",
                        color_discrete_sequence=["#0083B8"] * len(salesByTime),
                        template="plotly_white",
                        )
barChartByHour.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                             xaxis=(dict(showgrid=False)))

leftCOL, rightCOL = st.columns(2)
with leftCOL:
    st.plotly_chart(barChartByProductLine)
with rightCOL:
    st.plotly_chart(barChartByHour)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
