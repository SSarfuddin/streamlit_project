

import streamlit as st
import pandas as pd
import plotly.express as px


# Load data
@st.cache_data
def load_data():
    return pd.read_csv("Superstore.csv")

data = load_data()


# Sidebar for selecting the country, state, and city
country = st.sidebar.selectbox("Select Country", sorted(data['Country'].unique()))
state = st.sidebar.selectbox("Select State", sorted(data[data['Country'] == country]['State'].unique()))
city = st.sidebar.selectbox("Select City", sorted(data[data['State'] == state]['City'].unique()))



# Filter data based on selections
filtered_data = data[(data['Country'] == country) & (data['State'] == state) & (data['City'] == city)]


# Aggregate data for the selected filters
agg_data = filtered_data.groupby(['Country', 'State', 'City'])[["Sales", "Profit", "Discount"]].sum().reset_index()



# Melt the dataframe to get it into a long format
melted_data = agg_data.melt(id_vars=['Country', 'State', 'City'],
                            value_vars=['Sales', 'Profit', 'Discount'],
                            var_name='Metric', value_name='Amount')



# Display the bar plot
st.title("Sales, Profit, and Discount Analysis")

fig = px.bar(
    melted_data,
    x="Metric",
    y="Amount",
    color="Metric",
    title=f"{country} > {state} > {city}: Sales, Profit, and Discount",
    labels={"Amount": "Amount in USD"}
)


st.plotly_chart(fig)








