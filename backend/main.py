from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import joblib
import numpy as np
from datetime import datetime, date

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
cache = {}

@app.get("/")
def root():
    return{"message": "It is working!"}

@app.get("/current")
def get_current():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":LUKLA_LAT,
        "longitude":LUKLA_LON,
       "current": "temperature_2m,wind_speed_10m,wind_direction_10m,precipitation,cloud_cover,visibility,surface_pressure",        
        }
    
    res = requests.get(url,params = params).json()
    today = str(date.today())
    if "current" +today in cache:
        return cache["current"+ today]
    result = res.get("current",res)
    cache ["current"+today] = result
    return result

@app.get("/predict")
def predict():
    today = str(date.today())
    if "predict" + today in cache:
        return cache ["predict"+ today]
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude" : LUKLA_LAT,
        "longitude": LUKLA_LON,
        "hourly": "wind_speed_700hPa,wind_speed_850hPa,temperature_700hPa,temperature_850hPa",
        "forecast_days": 1
    }

    res = requests.get(url, params = params).json()
    if "hourly" not in res:
        return {"risk_score": 0.15, "label":"low"}
    hourly = res["hourly"]
    wind_700 = np.mean(hourly["wind_speed_700hPa"])
    wind_850 = np.mean(hourly["wind_speed_850hPa"])
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
    cache["predict" + today] = {"risk_score": round(risk_score, 4), "label":label}
    return{"risk_score": round(risk_score, 4),"label":label}


@app.get("/forecast")
def forecast():
    today = str(date.today())
    if "forecast" + today in cache:
        return cache["forecast" +today]
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude" : LUKLA_LAT,
        "longitude": LUKLA_LON,
        "hourly": "wind_speed_700hPa,wind_speed_850hPa,temperature_700hPa,temperature_850hPa",
        "forecast_days": 7
    }
    res = requests.get(url, params = params).json()
    if "hourly" not in res:
        return [{"day": i+1, "risk_score":0.15, "label": "Low"} for i in range(7)]
    hourly = res["hourly"]

    results = []
    for day in range(7):
        start = day*24
        end = start + 24

        wind_700 = np.mean(hourly["wind_speed_700hPa"][start:end])
        wind_850 = np.mean(hourly["wind_speed_850hPa"][start:end])
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
    
    
    
    cache["forecast" + today] = results
    return results
