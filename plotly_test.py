import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

dfConfirmed = pd.read_csv('time_series_covid19_confirmed_global.csv')
dfdeaths = pd.read_csv('time_series_covid19_deaths_global.csv')
dfrecovered = pd.read_csv('time_series_covid19_recovered_global.csv')
# print(globalConfirmedByCountries.head())
# print(globalConfirmedByCountries.columns)

# fig = go.Figure(data=go.Choropleth(
#     locations=df.columns,
#     text=df.columns,
# ))
# fig.show()
