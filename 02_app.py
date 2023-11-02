import streamlit as st
import requests
import pandas as pd

# Streamlit app title
st.title("Air Quality Data Viewer")

# Function to fetch data from the Flask API
def get_air_quality_data():
    response = requests.get('http://localhost:5000/air_quality_data')  # Replace with your Flask server URL
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: Unable to retrieve data. Status code: {response.status_code}")
        return []

# Fetch data from the Flask API
data = get_air_quality_data()

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Create a multiselect widget to allow column selection
st.sidebar.header("Select Columns to Display")
selected_columns = st.sidebar.multiselect(
    "Choose Columns",
    df.columns.tolist(),  # List of all available columns
    default=["Future_Date", "prediction_PM2_5", "prediction_PM10"] # Default selected columns
)

# Filter the DataFrame to include only selected columns
filtered_df = df[selected_columns]

# Display the data in Streamlit as a table
if not filtered_df.empty:
    st.write("Selected Columns:")
    st.table(filtered_df)
else:
    st.write("No data available.")
