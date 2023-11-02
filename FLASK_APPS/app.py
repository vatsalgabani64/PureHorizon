# Import the necessary modules and create an instance of the AirQualityData model (assuming you have already defined the model and created the database)
import pandas as pd
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///airquality.db'  # Replace with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)
CORS(app) 
# db.init_app(app)

class AirQualityData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Future_Date = db.Column(db.String)
    prediction_PM2_5 = db.Column(db.Float)
    prediction_PM10 = db.Column(db.Float)
    prediction_SO2 = db.Column(db.Float)
    prediction_CO = db.Column(db.Float)
    prediction_Ozone = db.Column(db.Float)
    prediction_NO2 = db.Column(db.Float)
    aqi_PM2_5 = db.Column(db.Float)
    aqi_PM10 = db.Column(db.Float)
    aqi_SO2 = db.Column(db.Float)
    aqi_CO = db.Column(db.Float)
    aqi_Ozone = db.Column(db.Float)
    aqi_NO2 = db.Column(db.Float)
    prediction_AQI = db.Column(db.Float)

@app.route('/')
def hello_world():
    df = pd.read_csv('predicted_updated.csv')

    for index, row in df.iterrows():
        new_data = AirQualityData(
        Future_Date=row['Future_Date'],
        prediction_PM2_5=row['prediction_PM2_5'],
        prediction_PM10=row['prediction_PM10'],
        prediction_SO2=row['prediction_SO2'],
        prediction_CO=row['prediction_CO'],
        prediction_Ozone=row['prediction_Ozone'],
        prediction_NO2=row['prediction_NO2'],
        aqi_PM2_5=row['aqi_PM2_5'],  # Note the field name adjustment with a period
        aqi_PM10=row['aqi_PM10'],
        aqi_SO2=row['aqi_SO2'],
        aqi_CO=row['aqi_CO'],
        aqi_Ozone=row['aqi_Ozone'],
        aqi_NO2=row['aqi_NO2'],
        prediction_AQI=row['prediction_AQI']
        )
        print("print new data")
        db.session.add(new_data)
        
    db.session.commit()
    
    # airQuality = AirQualityData(Future_Date = '2023-04-01 00:00:00',
    #     prediction_PM2_5= 30.495914459228516,
    #     prediction_PM10= 82.2533187866211,
    #     prediction_SO2= 19.128902435302734,
    #     prediction_CO= 0.9985187649726868,
    #     prediction_Ozone= 15.584328651428223,
    #     prediction_NO2= 66.0024185180664,
    #     aqi_PM2_5= 82.2533187866211,
    #     aqi_PM10= 23.911128044128418,
    #     aqi_SO2= 49.92593824863434,
    #     aqi_CO= 15.584328651428223,
    #     aqi_Ozone= 82.41329506116035,
    #     aqi_NO2= 82.41329506116035)
    # db.session.add(airQuality)
    return "Welcome to Flask Backend"

@app.route('/air_quality_data', methods=['GET'])
def get_air_quality_data():
    # Query the database to fetch the data from the model
    data = AirQualityData.query.all()

    # Convert the data to a list of dictionaries
    data_list = []
    for record in data:
        data_list.append({
            'id': record.id,
            'Future_Date': record.Future_Date,
            'prediction_PM2_5': record.prediction_PM2_5,
            'prediction_PM10': record.prediction_PM10,
            'prediction_SO2': record.prediction_SO2,
            'prediction_CO': record.prediction_CO,
            'prediction_Ozone': record.prediction_Ozone,
            'prediction_NO2': record.prediction_NO2,
            'aqi_PM2_5': record.aqi_PM2_5,
            'aqi_PM10': record.aqi_PM10,
            'aqi_SO2': record.aqi_SO2,
            'aqi_CO': record.aqi_CO,
            'aqi_Ozone': record.aqi_Ozone,
            'aqi_NO2': record.aqi_NO2,
            'prediction_AQI': record.prediction_AQI
        })

    return jsonify(data_list)

if __name__ == "__main__":
    app.run(debug=True)

