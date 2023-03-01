import streamlit as st
import altair as alt
import pandas as pd

st.title("CIVic Visualization Tool")

# load data 
df = pd.read_csv("data/civic_data.tsv")
df_unique = pd.read_csv("data/civic_data_unique.tsv")

### Number of Records of All Diseases Reported in a Year ###

# replace with st.slider
Year = st.slider("Year", min(df["year"]), max(df["year"]), value = 2018)
subset = df[df["year"] == Year]

plot1 = alt.Chart(subset).mark_bar().encode(
    x=alt.X('disease:N', title="Diseases", sort="-y"),
    y=alt.Y(aggregate = "count", type='quantitative', title="Number of Records")
).properties(
    title=f"Number of Records of All Diseases Reported in {Year}",
    width=600,
    height=600
)

st.altair_chart(plot1)