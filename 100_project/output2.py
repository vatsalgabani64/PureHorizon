import requests
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="PureHorizon", page_icon=":tada:", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")

# ---- LOAD ASSETS ----
lottie_coding = load_lottieurl("https://lottie.host/a96988fe-9d6f-448b-94c1-97b710cd53bf/Sg5SAAAUOw.json")
img_contact_form = Image.open("image_01.jpg")
img_lottie_animation = Image.open("image_01.jpg")

# ---- HEADER SECTION ----
st.subheader("Air Pollution Prediction & Visualization")
st.title("Python project")
st.write("PureHorizon is a platform that uses machine learning to predict air quality and visualize pollution data. It can be used to track air quality in real time, identify pollution hotspots, and forecast air quality conditions. PureHorizon is a valuable tool for businesses, governments, and individuals who need to make informed decisions about air quality.")
st.write("[More information about PureHorizon]()") # added link for more info of our project

# ---- WHAT I DO ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("What I do")
        st.write("##")
        st.write(
            """
            On my YouTube channel I am creating tutorials for people who:
            - are looking for a way to leverage the power of Python in their day-to-day work.
            - are struggling with repetitive tasks in Excel and are looking for a way to use Python and VBA.
            - want to learn Data Analysis & Data Science to perform meaningful and impactful analyses.
            - are working with Excel and found themselves thinking - "there has to be a better way."

            If this sounds interesting to you, consider subscribing and turning on the notifications, so you don’t miss any content.
            """
        )
        # st.write("[YouTube Channel >](https://youtube.com/c/CodingIsFun)")
    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")

# ---- PROJECTS ----
with st.container():
    st.write("---")
    st.header("Air Quality Analysis and Vizulization")
    st.write("##")
#     image_column, text_column = st.columns((1, 2))
#     with image_column:
#         st.image(img_lottie_animation)
#     with text_column:
#         st.subheader("Integrate Lottie Animations Inside Your Streamlit App")
#         st.write(
#             """
#             Learn how to use Lottie Files in Streamlit!
#             Animations make our web app more engaging and fun, and Lottie Files are the easiest way to do it!
#             In this tutorial, I'll show you exactly how to do it
#             """
#         )
        

# with st.container():
#     image_column, text_column = st.columns((1, 2))
#     # with image_column:
#     #     st.image(img_contact_form)
#     with text_column:
#         st.subheader("How To Add A Contact Form To Your Streamlit App")
#         st.write(
#             """
#             Want to add a contact form to your Streamlit website?
#             In this video, I'm going to show you how to implement a contact form in your Streamlit app using the free service ‘Form Submit’.
#             """
#         )
#         # st.markdown("[Watch Video...](https://youtu.be/FOULV9Xij_8)")
        
        
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
    st.header("Air Quality Prediction")

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

# ---- CONTACT ----
with st.container():
    st.write("---")
    st.header("Get In Touch With Me!")
    st.write("##")

    # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
    contact_form = """
    <form action="https://formsubmit.co/YOUR@MAIL.COM" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()