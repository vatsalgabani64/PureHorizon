import streamlit as st
# st.set_page_config(layout="wide")
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.markdown(
    """
    <style>
    # .full-width-plot {
    #     width: 70%;
    # }
    .st-eb {
        width: 50%;
    }
    table{
        border-collapse:collapse;
        width: 70%;
    }
    th, td {
        width: 50%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

df = pd.read_csv('predicted.csv')
standards = pd.read_csv('standard.csv')

def Home_screen():
    st.title("Air Quality Prediction")

def Analysis_screen():
    st.title('Predicted Pollutant Levels')
    pollutants = st.multiselect('Select pollutants', ['PM2.5','PM10','SO2','CO','Ozone','NO2','AQI'])
    if pollutants:
        df.set_index(df['Future_Date'],inplace=True)
        # st.write(df[pollutants])
        lst = [f'prediction_{x}' for x in pollutants]
        st.write(df[lst])
    

    # #df['Future_Date'] is now index of df ,inplace=true modifies df without creating new df
    # df.set_index(df['Future_Date'],inplace=True)
    # st.write(df)

    # #displays label 'PM2.5' with given value
    # # st.write('PM2.5', df['prediction_PM2.5 (ug/m3)'])
    # #display first few rows
    # st.write(df.head()) 

def Visualization_screen():
    
    df=pd.read_csv('predicted.csv')
    # cities = {'City':['Ahmedabad','Gandhinagar']}
    # cities = df2['City'].unique()
    # selected_city = st.selectbox('Select city', cities)

    # Filter the data to only include rows for the selected city
    # df2 = df2[df2['City'] == selected_city]

   # Sample list of options
    options = ['PM2.5','PM10','SO2','CO','Ozone','NO2','AQI']

    # Use st.selectbox
    selected_option = st.selectbox('Select pollutant :',  options)

    st.title('Scale')
    data={'Corresponding AQI':standards['AQI'],f'{selected_option}':standards[selected_option]}
    stand_df = pd.DataFrame(data)
    # st.table(stand_df)  
    # st.dataframe(df.set_index(df.columns[0]))   #works but no heading for a index column
    st.markdown(stand_df.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    st.title('Plot')
    # st.title('Visualization')
    plt.figure(figsize=(4,3))
    plt.plot(df[f'prediction_{selected_option}'])
    plt.xticks(rotation=80)
    st.pyplot(plt,use_container_width=False)

    





    # df2=pd.read_csv('air_quality_data.csv')
    # # cities = {'City':['Ahmedabad','Gandhinagar']}
    # cities = df2['City'].unique()
    # selected_city = st.selectbox('Select city', cities)

    # # Filter the data to only include rows for the selected city
    # df2 = df2[df2['City'] == selected_city]

    # # Create a multiselect widget to allow the user to select the pollutants to display
    # pollutants = st.multiselect('Select pollutants', ['PM2.5','PM10','NO','NO2','NOx','NH3','CO','SO2','O3','Benzene','Toluene','Xylene'])

    # Create a scatter plot to display the selected pollutants over time for each city
    # if pollutants:
    #     chart_data = df2.melt(id_vars=['Date', 'City'], value_vars=pollutants, var_name='pollutant', value_name='level')
    #     fig = px.scatter(chart_data, x='Date', y='level', color='pollutant')
    
    #     # Update the title of each subplot
    #     fig.update_layout({'xaxis1': {'title': {'text': f'Air Quality of {selected_city}'}}})
    
    #     st.plotly_chart(fig, width=800, height=600)
    
    # else:
    #     st.write('Please select at least one pollutant.')


selected = option_menu(
        menu_title='Main Menu',
        options=["Home","Analysis","Visualization"],
        # icons=["","",""],
        # menu_icon='',
        # default_index=0,
        orientation="horizontal",
        styles={"container":{"padding":"10px","margin":"0px"}}
    )
if selected == "Home":
    Home_screen()
if selected == "Analysis":
    Analysis_screen()
if selected == "Visualization":
    Visualization_screen()











