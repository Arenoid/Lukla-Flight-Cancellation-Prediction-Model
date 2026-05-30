import cdsapi
c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-pressure-levels',
    {
        'product_type':'reanalysis',
        'variable': ['u_component_of_wind', 'v_component_of_wind','temperature'],
        'pressure_level':['700','850'],
        'year':['2022'],
        'month':[f'{m:02d}' for m in range(1,13)],
        'day':[f'{d:02d}' for d in range(1,32)],
        'time': ['06:00', '09:00'],
        'area': [28.5, 86.0, 27.0, 87.5],
        'format':'netcdf'
    },
    'lukla_era5.nc'
)