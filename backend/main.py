from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import requests
import joblib
import numpy as np

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

LUKLA_LAT = 27.6869
LUKLA_LON = 86.7314

model = joblib.load("model.joblib")


@app.get("/")
def root():
    return{"message": "It is working!"}

@app.get("/current")
def get_current():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":LUKLA_LAT,
        "longitude":LUKLA_LON,
        "current": "temperature,windspeed,winddirection,precipitation,cloudcover,visibility,surface_pressure",
        "forecast_days":7
    }
    res = requests.get(url,params = params).json()
    return res["current"]


@app.get("/predict")
def predict():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude" : LUKLA_LAT,
        "longitude": LUKLA_LON,
        "hourly": "windspeed_700hPa,windspeed_850hPa,temperature_700hPa,temperature_850hPa",
        "forecast_days": 1
    }

    res = requests.get(url, params = params).json()
    hourly = res["hourly"]
    wind_700 = np.mean(hourly["windspeed_700hPa"])
    wind_850 = np.mean(hourly["windspeed_850hPa"])
    wind_shear = wind_700-wind_850
    temp_lapse = np.mean(hourly["temperature_850hPa"]) - np.mean(hourly["temperature_700hPa"])
    features = np.array([[wind_700, wind_850, wind_shear, temp_lapse, datetime.now().month]])
    risk_score = float(model.predict_proba(features)[0][1])
    if risk_score<0.3:
        label = "Low"
    elif risk_score<0.6:
        label = "Medium"
    else:
        label = "High"
    return{"risk_score": round(risk_score, 4),"label":label}


@app.get("/forecast")
def forecast():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude" : LUKLA_LAT,
        "longitude": LUKLA_LON,
        "hourly": "windspeed_700hPa,windspeed_850hPa,temperature_700hPa,temperature_850hPa",
        "forecast_days": 7
    }
    res = requests.get(url, params = params).json()
    hourly = res["hourly"]

    results = []
    for day in range(7):
        start = day*24
        end = start + 24

        wind_700 = np.mean(hourly["windspeed_700hPa"][start:end])
        wind_850 = np.mean(hourly["windspeed_850hPa"][start:end])
        wind_shear = wind_700 - wind_850
        temp_lapse = np.mean(hourly["temperature_850hPa"][start:end])-np.mean(hourly["temperature_700hPa"][start:end])

        features = np.array([[wind_700, wind_850, wind_shear, temp_lapse, datetime.now().month]])
        risk_score = float(model.predict_proba(features)[0][1])

        if risk_score <0.3:
            label = "low"
        elif risk_score <0.6:
            label = "medium"
        else:
            label = "high"

        results.append({
            "day":day + 1,
            "risk_score": round(risk_score, 4),
            "label": label
        })

    return results
