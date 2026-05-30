# Lukla Flight Cancellation Risk Prediction Model
> Provides a realtime prediction for flight cancellation for Lukla Airport(VNLK)

---

## Use Case
> Due to the airport being almost 3000m above sealevel, it has one of the highest flight cancellation rates in the world due to its unpredictable weather condtitions. This Dashboard uses a dataset of 2022, extracted from ERA5 to predict the probablity of flight cancellations for the next 7 days. (almost)

## ⚠FAIR WARNING
> The dataset for flight cancellations was not available on the internet, except on flightradr. To counter this i have used AI to generate the dataset of flight cancellations with utmost accurary. If you have a relaiable dataset you can train this model by replacing the `cancellations.csv` file with your own dataset. Just dont change the name.

## Screenshot

https://imgur.com/DysV07A

## DEMO
https://lukla-flight-cancellation-predictio.vercel.app/

## Workings

1. ERA5 data analysis from Copernicus (2022) provides wind speed at 700hPA and 850hPa pressure levels, wind shear, and temperature lapse rate for the region.

2. Flight cancellations records for 2022 used to train the model.

3. XGBOOST classifier was trained on atmospheric features, achieves - 65% accuracy.

4. OPEN METEO API is used to provide a realtime 7day forecast atmospheric data which was then fed into the model to generate risk scores.



# Running Locally

**Requirements**
- Python 3.10+
- Node.js 18+

**Backend**
```bash
cd backend
pip install fastapi uvicorn requests pandas numpy scikit-learn xgboost joblib xarray h5netcdf netcdf4 cdsapi
uvicorn main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm install recharts axios
npm run dev
```

Visit `https://localhosts:5123`

## Data From
- [ERA5 Reanalysis — Copernicus Climate Data Store](https://cds.climate.copernicus.eu)
- [Open-Meteo API](https://open-meteo.com)
