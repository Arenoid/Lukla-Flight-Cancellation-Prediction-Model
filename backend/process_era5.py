import xarray as xr
import pandas as pd

ds = xr.open_dataset(r"C:\Users\Mimansak Nepal\Documents\The Lukla Weather Risk Dashboard\backend\lukla_era5.nc")

u700 = ds['u'].sel(pressure_level=700).values.flatten()
u850 = ds['u'].sel(pressure_level = 850).values.flatten()
v700 = ds['v'].sel(pressure_level=700).values.flatten()
v850 = ds['v'].sel(pressure_level=850).values.flatten()
temp700 = ds['t'].sel(pressure_level=700).values.flatten()
temp850 = ds['t'].sel(pressure_level=850).values.flatten()

wind_speed_700 = (u700**2 + v700**2)**0.5
wind_speed_850 = (u850**2+v850**2)**0.5

wind_shear = wind_speed_700-wind_speed_850
temp_lapse = temp850-temp700

times = ds['valid_time'].values
times = times.repeat(ds.dims.get('latitude',1)* ds.dims.get('longitude',1))

df = pd.DataFrame({
    'time': times[:len(wind_shear)],
    'wind_speed_700':wind_speed_700,
    'wind_speed_850':wind_speed_850,
    'wind_shear':wind_shear,
    'temp_lapse':temp_lapse
})

df['date'] = pd.to_datetime(df['time']).dt.date
df = df.groupby('date').mean(numeric_only = True).reset_index()
df.to_csv('processed.csv',index = False)
print("Done! Rows:", len(df))
print(df.head())

