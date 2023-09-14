# Import necessary libraries
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium


# Load the datasets
@st.cache_data
def load_data():
    canada = pd.read_csv('Canada_Province_Unemployment.csv')
    gdf = gpd.read_file('canada.geojson')

    return canada, gdf

canada, gdf = load_data()


st.title("Public showcase of lazy Canadians")
st.sidebar.header("Filters 📊")

st.markdown("""
            Welcome to the lazy Canada dashboard.
""")
with st.expander("📊 **Objective**"):
                 st.markdown("""
Ever wondered if Canadians are embracing the fine art of lounging around in their picturesque locales? 🇨🇦   Well, we've got the scoop for you! Dive into our vibrant dashboard, where we unravel the mysteries surrounding the "chill" segment of the Canadian population. 🍁
In this thrilling saga, we embark on a journey to discover:
🌎 Are there pockets in Canada's HUGE and diverse landscapes where people are mastering the art of relaxation a bit more than others? Let's explore the unemployment rates across different geographical zones of Canada!

📈 Buckle up as we time travel through the ridiculously big (almost like 🇨🇦) data set to history to witness the evolution of unemployment rates in Canada.

Join us in this exciting adventure as we uncover the secrets behind the laid-back Canadians, one statistic at a time! Let's find out if Canadians are really leaning into the leisure life or if something else is behind it (law from 2018.). 🍁

Stay tuned!
"""
)
                           
with st.expander("**How to Use the Dashboard** 📚"):
    st.markdown("""
    1. **Filter Data** - Use the sidebar filters to narrow down specific datasets.
    2. **Visualize Data** - From the dropdown, select a visualization type to view patterns.
    3. **Map** - The map is not depending on the sidebar filters. To see the map, at least one age group and one geographical area must be chosen in the sidebar, though.
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

grouped_data = canada.groupby('GEO')[['Employment', 'Unemployment']].sum().reset_index()
grouped_data['Total_Workforce'] = grouped_data['Employment'] + grouped_data['Unemployment']
grouped_data['Employment_Percentage'] = (grouped_data['Employment'] / grouped_data['Total_Workforce']) * 100
grouped_data['Unemployment_Percentage'] = (grouped_data['Unemployment'] / grouped_data['Total_Workforce']) * 100


filtered_canada2 =filtered_df[filtered_df['REF_DATE'].str.endswith("12")]

alt.Chart(filtered_canada2).mark_line().encode(
    y = 'Unemployment rate:Q',
    x = 'REF_DATE:T',
    color=('GEO:N')
).properties(
    width=600,
    height=300,
    
)

# Dropdown to select the type of visualization - make a name for each chart.
visualization_option = st.selectbox(
    "Select Visualization 🎨", 
    ["The density of employment rate for different age groups", 
     "The density of employment rate for different geographical areas", 
     "Development of Unemployment by Geographical Area",
     "Employment and Unemployment Percentage by Province in Canada"] #stacked bar chart    
)


if visualization_option == "The density of employment rate for different age groups":
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=filtered_df, x='Employment rate', hue='Age group', fill=True, palette='Set2')
    plt.xlabel('Employment rate')
    plt.ylabel('Density')
    plt.title('The density of employment rate for different age groups')
    st.pyplot(plt)

    # Done ---Development of unemployment by graphical area plot
elif visualization_option == "Development of Unemployment by Geographical Area":

    filtered_canada2 =filtered_df[filtered_df['REF_DATE'].str.endswith("12")]

    chart2 = alt.Chart(filtered_canada2).mark_line().encode(
    y = 'Unemployment rate:Q',
    x = 'REF_DATE:T',
    color=('GEO:N')
    ).properties(
    width=600,
    height=300,
    )
    st.altair_chart(chart2, use_container_width=True)
elif visualization_option == "Employment and Unemployment Percentage by Province in Canada":
    st.subheader('Bar Chart')
    
    # Setting the positions and width for the bars
    pos = list(range(len(grouped_data['GEO']))) 
    width = 0.75 

    # Plotting the bars
    fig, ax = plt.subplots(figsize=(15, 7))
    plt.bar(pos, grouped_data['Employment_Percentage'], width, alpha=0.75, color='#57a773', label='Employment')
    plt.bar(pos, grouped_data['Unemployment_Percentage'], width, bottom=grouped_data['Employment_Percentage'], alpha=0.75, color='#ff6f61', label='Unemployment')
    
    # Customize the chart
    ax.set_ylabel('Percentage (%)', fontsize=12)
    ax.set_xticks(pos)
    ax.set_xticklabels(grouped_data['GEO'], rotation=90, fontsize=12)
    plt.xlim(min(pos)-width, max(pos)+width*4)
    plt.ylim([0, 100])
    plt.legend(loc='upper right', fontsize=12)
    plt.grid(axis='y')
    plt.axhline(y=50, color='gray', linestyle='--', linewidth=0.7)
    
    # Adding data labels
    for i, val in enumerate(grouped_data['Employment_Percentage']):
        plt.text(i, val/2, f"{val:.2f}%", ha='center', va='center', fontsize=10, color='white')
        plt.text(i, val + grouped_data['Unemployment_Percentage'][i]/2, f"{grouped_data['Unemployment_Percentage'][i]:.2f}%", ha='center', va='center', fontsize=10, color='white')
    
 
    
    st.pyplot(fig)

# Done The density of employment rate for different geographical areas
elif visualization_option == "The density of employment rate for different geographical areas":
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=filtered_df, x='Employment rate', hue='GEO', fill=True, palette='Set2')
    plt.xlabel('Employment rate')
    plt.ylabel('Density')
    plt.title('The density of employment rate for different geographical areas')
    st.pyplot(plt)
    





# The Maps monster
    st.header("Unemployment Map")
with st.expander("**How to Use the Map below** 🌎"):
    st.markdown("""
    Click on the markers on the map to explore the employment rate, participation rate, and unemployment rate for different age groups in the different states of Canada. All data in the map is from January 2023.
    Zoom in on an area till you get the blue dots. These you can click, and a textbox will popup with information about the population of the state. 
    """)

    #Create GeoDataFrame
    gdf_canada = gpd.GeoDataFrame(canada, geometry=gpd.points_from_xy(canada['Longitude'], canada['Latitude']))
    gdf_canada.crs = "EPSG:4326"

    gdf_canada = gdf_canada.to_crs("EPSG:4326")

    pd.to_numeric(gdf_canada['Latitude'])
    pd.to_numeric(gdf_canada['Longitude'])

    df_filtered = gdf_canada[gdf_canada['REF_DATE'] == '2023-01']
    df_filtered = df_filtered[df_filtered['Age group'] != '15 to 64 years']
    df_filtered = df_filtered[df_filtered['Age group'] != '25 years and over']
    df_filtered = df_filtered[df_filtered['Age group'] != '15 years and over']

    m = folium.Map(location=[52.7362, -88.4568], zoom_start=3, tiles="CartoDB positron")

    # Create a marker cluster
    marker_cluster = MarkerCluster().add_to(m)

    # Loop through each police shooting and add it as a circle on the map within the marker cluster
    for _, row in df_filtered.iterrows():
        # Creating a pop-up message with some key information about the incident
        popup_content = f"""
        State: {row['GEO']}<br>
        Age group: {row['Age group']}<br>
        Population count: {row['Population']}<br>
        Employment rate: {row['Employment rate']}<br>
        Participation rate: {row['Participation rate']}<br>
        Unemployment rate: {row['Unemployment rate']}<br>
        """
        popup = folium.Popup(popup_content, max_width=300)
            
        folium.Circle(
            location=[row['Latitude'], row['Longitude']],
            radius=15,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.4,
            popup=popup
        ).add_to(marker_cluster)

    st_folium(m, width=725, height=300)

# the end 

with st.expander("**Example of lazy Canadians in their natural habitat** 📚"):
    st.markdown("**Doggo** (doggo.jpg)")

