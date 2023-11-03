#Import required libraries
import re
import os
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
import requests
from bs4 import BeautifulSoup

#defining required functions and configurations
st.set_page_config(page_title="PureHorizon", page_icon=":tada:", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#apply CSS
with open("styles.css") as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
lottie_coding = load_lottieurl("https://lottie.host/a96988fe-9d6f-448b-94c1-97b710cd53bf/Sg5SAAAUOw.json")

#------------------PROJECT CODE STARTS HERE-----------------------------------

# ---- HEADER SECTION ----
def header():
    st.title("PureHorizon")
    st.subheader("Air Pollution Prediction & Visualization")
    st.write("PureHorizon is a platform that uses machine learning to predict air quality and visualize pollution data. It can be used to track air quality in real time, identify pollution hotspots, and forecast air quality conditions. PureHorizon is a valuable tool for businesses, governments, and individuals who need to make informed decisions about air quality.")

# ---- PROJECT DESCRIPTION ----
def description():
    with st.container():
        st.write("---")
        left_column, right_column = st.columns([3,2])
        with left_column:
            st.header("What We do")
            # st.write("#")
            st.subheader('Air Quality Prediction')
            st.write('Air Quality Prediction throgh LSTM')
            st.subheader('Data Analysis')
            st.write('AQI analysis with Central Pollution Control Board(CPCB) specified methods')
            st.subheader('Data Visualization')
            st.write('Data Visualization for pollutants and AQI index')
            st.subheader('Live News')
            st.write('Get Live news updates regarding weather situations')
            st.subheader('Email Updates')
            st.write('Get regular weather mails to keep track of current weather situations')
        
    
        with right_column:
            st.write("###")
            st.write('<style>div[data-widget="stLottie"] { background-color: red; height:400px; width:400px;}</style>', unsafe_allow_html=True)
        
            st_lottie(lottie_coding, height=300, key="coding")

# ---- MENU SCREENS ----
def News_screen():
    custom_css = """
    <style>
    a {
        color: white !important; /* Set link color to white */
        text-decoration: none !important; /* Remove underline */
    }
    </style>
    """

    # Apply the custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)


    url = "https://news.google.com/search?q=ahmedabad%20weather&hl=en-IN&gl=IN&ceid=IN%3Aen"  # Replace with the URL of the weather news page
    # st.header("Today's Gandhinagar Weather News")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        weather_news = soup.find_all("article")  # Modify class name accordingly
        # print(weather_news)
        # 4. Print or store the extracted data
        for news in weather_news[:5]:
            article = news.find("a")
            link = "https://news.google.com/"+((article["href"])[2:])
            headline = news.find("h3").text
            # st.subheader(f"{headline}")
              # Replace with the URL you want to open

            # if st.header("Click to open the website"):
            st.subheader(f"[{headline}]({link})")
            # print(f"Link: {link}")
    else:
        st.write("Failed to retrieve the webpage. Status code:", response.status_code)

def Analysis_screen():

    #custom CSS 
    st.markdown(
        """
        <style>
        div[data-baseweb="select"] {
            font-size:15px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    #Read dataset from CSV 
    df=pd.read_csv(f'FLASK_APPS/predicted_Gandhinagar.csv')
    
    st.title('Predicted Pollutant Levels')
    st.subheader("Select Pollutant")

    # Prompt user to select pollutant to view dataset of
    pollutants = st.multiselect('', ['AQI','PM2_5','PM10','SO2','CO','Ozone','NO2'])
    
    if pollutants:
        df.set_index(df['Future_Date'],inplace=True)
        lst = [f'prediction_{x}' for x in pollutants]
        lst = ['Future_Date'] + lst[0:]
        st.markdown(df[lst].style.hide(axis="index").to_html(), unsafe_allow_html=True)
    else:
        df.set_index(df['Future_Date'],inplace=True)
        lst = ['prediction_AQI']
        lst = ['Future_Date'] + lst[0:]
        st.markdown(df[lst].style.hide(axis="index").to_html(), unsafe_allow_html=True)

def Visualization_screen():

    #Read dataset from CSV 
    df=pd.read_csv(f'FLASK_APPS/predicted_Gandhinagar.csv')

    # Prompt user to select pollutant
    pollutant_options = ['AQI','PM2_5','PM10','SO2','CO','Ozone','NO2']
    selected_pollutant = st.selectbox('Select pollutant :',  pollutant_options)

    #Scale of values (mapped with AQI levels)
    st.title('Scale')
    standards = pd.read_csv('standard.csv')
    data={'Corresponding AQI':standards['AQI'],f'{selected_pollutant}':standards[selected_pollutant]}
    stand_df = pd.DataFrame(data)
    st.markdown(stand_df.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    #Plot of predicted values
    st.title('Plot')
    plt.figure(figsize=(4,3))
    plt.plot(df['Future_Date'],df[f'prediction_{selected_pollutant}'])
    plt.xticks(rotation=80,fontsize=5)
    rng=int(df[f'prediction_{selected_pollutant}'].max() - df[f'prediction_{selected_pollutant}'].min())
    if rng<5:
        step_size=1
    elif rng<=20:
        step_size=int(rng/2)
    elif rng<=30:
        step_size=int(rng/3)
    else:
        step_size=int(rng/5)
    plt.yticks(range(int(df[f'prediction_{selected_pollutant}'].min()), int(df[f'prediction_{selected_pollutant}'].max()) + step_size, step_size))
    plt.title(f'{selected_pollutant}')
    plt.xlabel('Timestamp')
    if selected_pollutant == "AQI":
        plt.ylabel('units')
    else:
        plt.ylabel('ug/m3')
    st.pyplot(plt,use_container_width=False)

# ---- MENUBAR -----
def Menu_header():
    with st.container():
        st.write("---")
        st.header("Air Quality Analysis and Visulization")
        st.write("##")

# ---- CONTACT FORM ----
def contact_form():

    #Load env which contains smtp details
    load_dotenv()

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

    # Streamlit Form
    st.write('')
    st.write("---")
    st.title("Subscribe")
    st.write("Join in to get daily weather updates")
    with st.form("Contact Form"):

        # Get data from the form
        name = st.text_input("Your name")
        email = st.text_input("Your email")
    
        df=pd.read_csv(f'FLASK_APPS/predicted_Gandhinagar.csv')
        highest_AQI_index = df['Future_Date'][df['prediction_AQI'].idxmax()]
        lowest_time = re.split(r'[:\s-]', highest_AQI_index)

        if st.form_submit_button("Submit"):
            if not email or not name:
                st.error("Empty fields detected")
            else:
                # Insert data into the database
                cursor.execute("INSERT INTO contact_data (name, email) VALUES (?, ?)", (name, email))
                conn.commit()

                # Email configurations
                smtp_server = 'smtp.gmail.com'
                smtp_port = 587
                smtp_username = 'purehorizonapp@gmail.com'
                smtp_password = os.getenv('smtp_pass')
                sender_email = 'purehorizonapp@gmail.com'
                recipient_email = f'{email}'

                #Email Format
                subject = 'Hello from PureHorizon'
                email_text = f"Hey,{name}\nYou just subscribed to the best weather forecasting services in the city.\n\nHere's some tips for the day:\n\nAir Quality is at its lowest at around {lowest_time[3]}:{lowest_time[4]} on {lowest_time[0].lstrip('0')}/{lowest_time[1].lstrip('0')}"


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

                st.success("Welcome to PureHorizon!")

            
    # Close the database connection 
    conn.close()

if __name__=='__main__':

    header()
    description()
    Menu_header()

    selected = option_menu(
        menu_title='',
        options=["News","Analysis","Visualization"],
        orientation="horizontal",
        styles={"container":{"padding":"10px","margin":"0px"}}
    )

    if selected == "News":
        News_screen()
    elif selected == "Analysis":
        Analysis_screen()
    elif selected == "Visualization":
        Visualization_screen()
    contact_form()