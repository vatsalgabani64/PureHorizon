import re
import requests
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import os

st.set_page_config(page_title="PureHorizon", page_icon=":tada:", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Use local CSS
# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# local_css("style.css")
# st.markdown(
#     f'<style>{open("style.css").read()}</style>',
#     unsafe_allow_html=True,
# )

css = '''
.stApp {
    # background: black   ;
    # background-size: cover;
    # background-position: center;
    # background-color: #333;
    # color: white;
    background: url('https://images.unsplash.com/photo-1487621167305-5d248087c724?auto=format&fit=crop&q=80&w=1932&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
}
.stApp > header {
    background-color: transparent;
}
a.link-class {
    color: red; /* Change the desired link color here */
}
.st-my-custom-class a{
    color: blue;

}
'''
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
# st.markdown(f'<style>{open("style.css").read()}</style>', unsafe_allow_html=True)
# ---- LOAD ASSETS ----
lottie_coding = load_lottieurl("https://lottie.host/a96988fe-9d6f-448b-94c1-97b710cd53bf/Sg5SAAAUOw.json")
img_contact_form = Image.open("image_01.jpg")
img_lottie_animation = Image.open("image_01.jpg")

# ---- HEADER SECTION ----
st.title("PureHorizon")
st.subheader("Air Pollution Prediction & Visualization")
st.write("PureHorizon is a platform that uses machine learning to predict air quality and visualize pollution data. It can be used to track air quality in real time, identify pollution hotspots, and forecast air quality conditions. PureHorizon is a valuable tool for businesses, governments, and individuals who need to make informed decisions about air quality.")
# st.write("[More informatio  n about PureHorizon]()") # added link for more info of our project
st.markdown("<div class='st-my-custom-class'><a href='https://purehorizon.streamlit.app'>More information about PureHorizon</a></div>", unsafe_allow_html=True)
# ---- WHAT WE DO ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns([2,1])
    with left_column:
        st.header("What We do")
        st.write("##")
        st.write(
            """
            - Data Analysis through Central Pollution Control Board(CPCB) specified methods for AQI calculation
            - Air Quality Prediction throgh LSTM 
            - Data Visualization for pollutants and AQI index
            """
        )
    with right_column:
        st.write('<style>div[data-widget="stLottie"] { background-color: lightblue; }</style>', unsafe_allow_html=True)
        
        st_lottie(lottie_coding, height=300, key="coding")

# ---- PROJECTS ----
with st.container():
    st.write("---")
    st.header("Air Quality Analysis and Visulization")
    st.write("##")
        

standards = pd.read_csv('standard.csv')

def Home_screen():
    st.subheader("Air Quality Prediction")
    st.write(
        """
        The following properties have been worked upon:
        - PM2.5
        - PM10
        - SO2
        - CO
        - Ozone 
        - NO2
        - AQI
        """
    )

def Analysis_screen():
    st.title('Predicted Pollutant Levels')

    # Sample list of options
    city_options = ['Gandhinagar','Ahmedabad']

    st.markdown(
        """
        <style>
        div[data-baseweb="select"] {
            font-size:25px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Select City")
    selected_city = st.selectbox(label='',options=city_options)
    df=pd.read_csv(f'predicted_{selected_city}.csv')

    st.subheader("Select Pollutant")
    pollutants = st.multiselect('', ['AQI','PM2.5','PM10','SO2','CO','Ozone','NO2'])

    if selected_city:
        highest_score_index = df['Future_Date'][df['prediction_AQI'].idxmax()]
        split_string = re.split(r'[:\s-]', highest_score_index)
        st.write(f"Highest AQI obeserved : {split_string[3]}:{split_string[4]} on {split_string[2]}/{split_string[1]}")
        highest_score_index = df['Future_Date'][df['prediction_AQI'].idxmin()]
        split_string = re.split(r'[:\s-]', highest_score_index)
        st.write(f"Lowest AQI obeserved : {split_string[3]}:{split_string[4]} on {split_string[2]}/{split_string[1]}")

    
    if pollutants:
        df.set_index(df['Future_Date'],inplace=True)
        lst = [f'prediction_{x}' for x in pollutants]
        lst = ['Future_Date'] + lst[0:]
        st.markdown(df[lst].style.hide(axis="index").to_html(), unsafe_allow_html=True)
        # st.write(df[lst])

def Visualization_screen():
    # Sample list of options
    city_options = ['Gandhinagar','Ahmedabad']

    # Use st.selectbox
    selected_city = st.selectbox('Select City :',  city_options)
    df=pd.read_csv(f'predicted_{selected_city}.csv')

    # Sample list of options
    pollutant_options = ['PM2.5','PM10','SO2','CO','Ozone','NO2','AQI']

    # Use st.selectbox
    selected_pollutant = st.selectbox('Select pollutant :',  pollutant_options)

    st.title('Scale')
    data={'Corresponding AQI':standards['AQI'],f'{selected_pollutant}':standards[selected_pollutant]}
    stand_df = pd.DataFrame(data)
    st.markdown(stand_df.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    st.title('Plot')
    plt.figure(figsize=(4,3))
    plt.plot(df[f'prediction_{selected_pollutant}'])
    plt.xticks(rotation=80)
    st.pyplot(plt,use_container_width=False)

selected = option_menu(
        menu_title='Main Menu',
        options=["Home","Analysis","Visualization"],
        orientation="horizontal",
        styles={"container":{"padding":"10px","margin":"0px"}}
    )
if selected == "Home":
    Home_screen()
if selected == "Analysis":
    Analysis_screen()
if selected == "Visualization":
    Visualization_screen()

def configure():
    load_dotenv()

configure()


# Database Connection
conn = sqlite3.connect('form_data.db')
cursor = conn.cursor()

# Create a table to store form data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS contact_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT
    )
''')

# Streamlit app
st.title("Subscribe")
st.write("Join in to get daily weather updates")
with st.form("Contact Form"):
    city_options = ['Gandhinagar','Ahmedabad']

    # Get data from the form
    name = st.text_input("Your name")
    email = st.text_input("Your email")
    selected_city = st.selectbox('Select City :',  city_options)
    
    
    df=pd.read_csv(f'predicted_{selected_city}.csv')
    highest_AQI_index = df['Future_Date'][df['prediction_AQI'].idxmax()]
    lowest_time = re.split(r'[:\s-]', highest_AQI_index)
    # st.write(split_string)

    if st.form_submit_button("Send"):
        # Insert data into the database
        cursor.execute("INSERT INTO contact_data (name, email) VALUES (?, ?)", (name, email))
        conn.commit()

        # Send an email
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'gabanivatsal17@gmail.com'
        smtp_password = os.getenv('smtp_pass')
        sender_email = 'gabanivatsal17@gmail.com'
        recipient_email = f'{email}'

        subject = 'Hello from PureHorizon'
        email_text = f"Hey,{name}\nYou just subscribed to the best weather forecasting services in the city.\n\nHere's some tips for the day:\n\nAir Quality is at its lowest at around {lowest_time[3]}:{lowest_time[4]} on {lowest_time[2]}th"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(email_text, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        st.success("Your message has been sent!")

# Close the database connection when you're done
conn.close()