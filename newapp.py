import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

# Read the files
dfConfirmed = pd.read_csv("confirmed.csv").drop("Unnamed: 0", axis=1)
dfDeaths = pd.read_csv("deaths.csv").drop("Unnamed: 0", axis=1)
dailyGlobalNewCases = pd.read_csv("dailyGlobalNewCases.csv")
dfActive = pd.read_csv("active.csv").drop("Unnamed: 0", axis=1)
dfRecovered = pd.read_csv("recovered.csv").drop("Unnamed: 0", axis=1)
dfgbConfirmed = pd.read_csv("globalTtl.csv").drop("Unnamed: 0", axis=1)

listOfCountries = list(dfConfirmed.columns[1:])
optCountries = []
for country in listOfCountries:
    dic = {"label": country, "value": country}
    optCountries.append(dic)