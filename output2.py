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


local_css("style.css")

# ---- LOAD ASSETS ----
lottie_coding = load_lottieurl("https://lottie.host/a96988fe-9d6f-448b-94c1-97b710cd53bf/Sg5SAAAUOw.json")
img_contact_form = Image.open("image_01.jpg")
img_lottie_animation = Image.open("image_01.jpg")

# ---- HEADER SECTION ----
st.title("PureHorizon")
st.subheader("Air Pollution Prediction & Visualization")
st.write("PureHorizon is a platform that uses machine learning to predict air quality and visualize pollution data. It can be used to track air quality in real time, identify pollution hotspots, and forecast air quality conditions. PureHorizon is a valuable tool for businesses, governments, and individuals who need to make informed decisions about air quality.")
st.write("[More information about PureHorizon]()") # added link for more info of our project

# ---- WHAT I DO ----
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
        # st.write("[YouTube Channel >](https://youtube.com/c/CodingIsFun)")
    with right_column:
        st.write('<style>div[data-widget="stLottie"] { background-color: lightblue; }</style>', unsafe_allow_html=True)
        
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
    # *{
    #     background-color: #FF99FF;
    #     color: black;
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
    div[data-widget="stOptionMenu"] .stOptionMenu {
        color:white;
        padding: 10px;
        margin: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

df = pd.read_csv('predicted.csv')
standards = pd.read_csv('standard.csv')

def Home_screen():
    st.header("Air Quality Prediction")
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
    st.markdown("""
        <style>
            .multiselect label span {
                color: red; /* Change the text color to red */
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title('Predicted Pollutant Levels')
    pollutants = st.multiselect('Select pollutants', ['PM2.5','PM10','SO2','CO','Ozone','NO2','AQI'])
    if pollutants:
        df.set_index(df['Future_Date'],inplace=True)
        # st.write(df[pollutants])
        lst = [f'prediction_{x}' for x in pollutants]
        st.write(df[lst])

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
# with st.container():
#     st.write("---")
#     st.header("Get In Touch With Me!")
#     st.write("##")

#     # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
#     contact_form = """
#     <form action="https://formsubmit.co/YOUR@MAIL.COM" method="POST">
#         <input type="hidden" name="_captcha" value="false">
#         <input type="text" name="name" placeholder="Your name" required>
#         <input type="email" name="email" placeholder="Your email" required>
#         <textarea name="message" placeholder="Your message here" required></textarea>
#         <button type="submit">Send</button>
#     </form>
#     """
#     left_column, right_column = st.columns(2)
#     with left_column:
#         st.markdown(contact_form, unsafe_allow_html=True)
#     with right_column:
#         st.empty()

import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

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
st.title("Contact Form")
with st.form("Contact Form"):
    # Get data from the form
    name = st.text_input("Your name")
    email = st.text_input("Your email")
    message = st.text_area("Your message")

    if st.form_submit_button("Send"):
        # Insert data into the database
        cursor.execute("INSERT INTO contact_data (name, email, message) VALUES (?, ?, ?)", (name, email, message))
        conn.commit()

        # Send an email
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'gabanivatsal17@gmail.com'
        smtp_password = 'rpob ahoz tavo ujwg'
        sender_email = 'gabanivatsal17@gmail.com'
        recipient_email = f'{email}'

        subject = 'Copy of Feedback'
        email_text = f"Hey,{name}\nYour Feedback has been successfully sent.\nHere's a copy of your response:\n{message}"

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