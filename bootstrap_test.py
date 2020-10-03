import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

# Read files
dfConfirmed = pd.read_csv("confirmed.csv").drop("Unnamed: 0", axis=1).set_index("Date")
dfDeaths = pd.read_csv("deaths.csv").drop("Unnamed: 0", axis=1).set_index("Date")
dfActive = pd.read_csv("active.csv").drop("Unnamed: 0", axis=1).set_index("Date")
dfRecovered = pd.read_csv("recovered.csv").drop("Unnamed: 0", axis=1).set_index("Date")
dailyGlobalNewCases = (
    pd.read_csv("dailyGlobalNewCases.csv").drop("Unnamed: 0", axis=1).set_index("Date")
)
dfgbConfirmed = (
    pd.read_csv("globalTtl.csv").drop("Unnamed: 0", axis=1).set_index("Date")
)

# Create a list of countries for the dropdown menu
listOfCountries = list(dfConfirmed.columns)
optCountries = []
for country in listOfCountries:
    dic = {"label": country, "value": country}
    optCountries.append(dic)

# Global Data Graph
countryAndCases = dict(
    zip(dfConfirmed.columns.tolist(), dfConfirmed.iloc[-1, :].tolist())
)
topTen = sorted(countryAndCases.items(), key=lambda x: x[1], reverse=True)[0:10]
xValue = [topTen[i][1] for i in range(10)][::-1].copy()
yValue = [topTen[i][0] for i in range(10)][::-1].copy()

# Calculate global ttl, dnc, atc
TTL = str(round(dfConfirmed.iloc[-1, :].sum() / 1000000, 2)) + "M"
DNC = str(round(dailyGlobalNewCases.iloc[-1, :].sum() / 1000, 2)) + "K"
ATC = str(round(dfActive.iloc[-1, :].sum() / 1000000, 2)) + "M"

# ------- app start from here -------

app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])

app.layout = 

@app.callback(
    Output(component_id="chosenGraph", component_property="figure"),
    [
        Input(component_id="countryDropdown", component_property="value"),
        Input(component_id="graphSelection", component_property="value"),
    ],
)
def update_figure(countryDropdown, graphSelection):
    if graphSelection == "TTC":
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(
            go.Bar(x=dfConfirmed.index, y=dfConfirmed[countryDropdown]), row=1, col=1
        )
        return fig
    elif graphSelection == "DNC":
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(
            go.Bar(x=dailyGlobalNewCases.index, y=dailyGlobalNewCases[countryDropdown]),
            row=1,
            col=1,
        )
        return fig
    elif graphSelection == "ATC":
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(
            go.Bar(x=dfActive.index, y=dfActive[countryDropdown]),
            row=1,
            col=1,
        )
        return fig



if __name__ == "__main__":
    app.run_server(debug=False)