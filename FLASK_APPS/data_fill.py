import pandas as pd

# Replace 'your_data.csv' with the path to your CSV file
df = pd.read_csv('predicted.csv')

columns_to_fill = [
    'prediction_PM2.5', 'prediction_PM10', 'prediction_SO2',
    'prediction_CO', 'prediction_Ozone', 'prediction_NO2',
    'aqi_PM2.5', 'aqi_PM10', 'aqi_SO2', 'aqi_CO',
    'aqi_Ozone', 'aqi_NO2', 'prediction_AQI'
]

# Update the specified columns with their respective mean values
for column in columns_to_fill:
    df[column] = df[column].fillna(df[column].mean())
df.to_csv('predicted_updated.csv', index=False)