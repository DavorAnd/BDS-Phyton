# Import necessary libraries
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster

# Load the datasets
@st.cache_data
def load_data():
    canada = pd.read_csv('Canada_Province_Unemployment.csv')
    gdf = gpd.read_file('https://raw.githubusercontent.com/aaubs/ds-master/main/data/geopandas_data/Neighborhood_Map_Atlas_Districts.geojson')
    return canada, gdf

canada, gdf = load_data()

st.title("Public showcase of lazy Canadians")
st.sidebar.header("Filters 📊")

st.markdown("""
            Welcome to the lazy Canada dashboard.
""")
with st.expander("📊 **Objective**"):
                 st.markdown("""
At the heart of this dashboard the data about data about Canadinas with emphasis on lazy part of population, and hope that it shows what it should :
- Are there different unemployment rates for the different geografical areas of Canada?
- How has the unemployment rate developed over time?
"""
)
                           
with st.expander("**How to Use the Dashboard** 📚"):
    st.markdown("""
    1. **Filter Data** - Use the sidebar filters to narrow down specific datasets.
    2. **Visualize Data** - From the dropdown, select a visualization type to view patterns.
    """)
# age groups
age_group_cat = {
      'Young':['15 to 24 years','15 to 19 years','20 to 24 years'],
      'Old':['55 to 64 years'],
      'Middle Age' : ['25 to 54 years'],
      'All Ages' : ['15 years and over']
}
#Selection for age groups in the sidebar
selected_age_group = st.sidebar.selectbox("Select Age Groups 🕰️",list(age_group_cat.keys()))
if not selected_age_group:
    st.warning("Please select an age group from the sidebar ⚠️")
    st.stop()
selected_age_group_list = age_group_cat[selected_age_group]
filtered_df =canada[canada['Age group'].isin(selected_age_group_list)]

# Geo selection

area = canada['GEO'].unique().tolist()
selected_area = st.sidebar.multiselect("Select Geografical Area 🌎", area, default=area)
if not selected_area:
    st.warning("Please select a geografical area from the sidebar ⚠️")
    st.stop()
filtered_df = filtered_df[filtered_df['GEO'].isin(selected_area)]
#Type of employment 





# Dropdown to select the type of visualization - make a name for each chart.


#Work until here -- missing the types of plots and polt code---


# Dropdown to select the type of visualization - make a name for each chart.
visualization_option = st.selectbox(
    "Select Visualization 🎨", 
    ["Unemployment by Age Group",
     "The density of employment rate for different age groups", 
     "The density of employment rate for different geographical areas"] #stacked bar chart    
)


if visualization_option == "Unemployment by Age Group":
    # Bar chart for unemployment by age group
    chart = alt.Chart(filtered_df).mark_bar().encode(
        x='Age group',
        y='count()',
        color='Unemployment rate'
    ).properties(
        title='Unemployment by Age Group'
    )
    st.altair_chart(chart, use_container_width=True)

elif visualization_option == "The density of employment rate for different age groups":
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=filtered_df, x='Employment rate', hue='Age group', fill=True, palette='Set2')
    plt.xlabel('Employment rate')
    plt.ylabel('Density')
    plt.title('The density of employment rate for different age groups')
    st.pyplot(plt)
