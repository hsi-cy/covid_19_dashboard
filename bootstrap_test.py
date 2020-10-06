import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc


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

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

"""NavBar Start"""
nav_item = dbc.NavItem(
    dbc.NavLink(
        "Data Source",
        href="https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series",
    )
)

# make a reuseable dropdown for the different examples
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem(
            "Project GitHub",
            href="https://github.com/hsi-cy/covid_19_dashboard",
        ),
        dbc.DropdownMenuItem(
            "LinkedIn", href="https://www.linkedin.com/in/cheng-yun-hsi-b586b5178/"
        ),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Plotly / Dash", href="https://dash.plot.ly/"),
        dbc.DropdownMenuItem(
            "Dash Bootstrap",
            href="https://dash-bootstrap-components.opensource.faculty.ai/",
        ),
    ],
    nav=True,
    in_navbar=True,
    label="Important Links",
)

# Navbar Layout
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.H2(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.NavbarBrand("COVID-19 Dashboard", className="ml-2")
                        ),
                    ],
                    align="center",
                    no_gutters=True,
                )
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [
                        nav_item,
                        dropdown,
                    ],
                    className="ml-auto",
                    navbar=True,
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-5",
)
"""NavBar End"""

###########################################

"""App Components Start"""
# body part

# Cards for TTL, DNC, ATC
cardTTL = dbc.Card(
    dbc.CardBody(
        [
            html.H4("COVID-19 Cases", className="card-title"),
            html.H2(TTL, className="card-subtitle"),
        ]
    ),
    style={"width": "18rem"},
)
cardDNC = dbc.Card(
    dbc.CardBody(
        [
            html.H4("COVID-19 Cases", className="card-title"),
            html.H2(DNC, className="card-subtitle"),
        ]
    ),
    style={"width": "18rem"},
)

cardATC = dbc.Card(
    dbc.CardBody(
        [
            html.H4("COVID-19 Cases", className="card-title"),
            html.H2(ATC, className="card-subtitle"),
        ]
    ),
    style={"width": "18rem"},
)

topTenGraph = html.Div(
    [
        dcc.Graph(
            id="topTenGraph",
            figure=go.Figure(go.Bar(x=xValue, y=yValue, orientation="h")),
        )
    ],
    className="topTenGraph",
)

graphConfirmed = html.Div(
    [
        dcc.Graph(
            id="confirmedGraph",
            figure=go.Figure(
                data=[
                    go.Bar(
                        x=dfConfirmed.index,
                        y=dfConfirmed[yValue[-1]],
                    )
                ],
                layout=go.Layout(
                    title=go.layout.Title(text=yValue[-1] + " Total Confirmed Cases")
                ),
            ),
        )
    ],
    className="graph",
)
graphDailyNew = html.Div(
    [
        dcc.Graph(
            id="dailyNewGraph",
            figure=go.Figure(
                data=[
                    go.Bar(
                        x=dailyGlobalNewCases.index,
                        y=dailyGlobalNewCases[yValue[-1]],
                    )
                ],
                layout=go.Layout(
                    title=go.layout.Title(text=yValue[-1] + " Daily New Cases")
                ),
            ),
        )
    ],
    className="graph",
)

graphActive = html.Div(
    [
        dcc.Graph(
            id="activeGraph",
            figure=go.Figure(
                data=[
                    go.Bar(
                        x=dfActive.index,
                        y=dfActive[yValue[-1]],
                    )
                ],
                layout=go.Layout(
                    title=go.layout.Title(text=yValue[-1] + " Active Cases")
                ),
            ),
        )
    ],
    className="graph",
)


###############################
dropdown = html.Div(
    [
        dcc.Dropdown(
            id="countryDropdown",
            options=optCountries,
        )
    ],
    className="dropdown",
)

radioItems = html.Div(
    [
        dcc.RadioItems(
            options=[
                {
                    "label": "Total Cases",
                    "value": "TTC",
                },
                {
                    "label": "Daily New Cases",
                    "value": "DNC",
                },
                {
                    "label": "Active Cases",
                    "value": "ATC",
                },
            ],
            id="graphSelection",
            value="TTC",
            labelStyle={"display": "inline-block"},
        )
    ],
    className="radioItems",
)

graph = html.Div(
    [
        dcc.Graph(
            id="chosenGraph",
            figure=go.Figure(
                data=[
                    go.Bar(
                        x=dfConfirmed.index,
                        y=dfConfirmed[yValue[-1]],
                    )
                ],
                layout=go.Layout(title=go.layout.Title(text=yValue[-1])),
            ),
        )
    ],
    className="graph",
)


"""App Components End"""

###########################################

"""App Layout"""
app.layout = html.Div(
    [
        navbar,
        dbc.Container(
            dbc.Row(
                [
                    dbc.Col([cardTTL, cardDNC, cardATC], width=3),
                    dbc.Col(topTenGraph, width=3),
                    dbc.Col(
                        [
                            graphConfirmed,
                            graphDailyNew,
                            graphActive,
                        ],
                        width=6,
                    ),
                ]
            )
        ),
    ]
)

"""Callback Start"""


"""Callback End"""

if __name__ == "__main__":
    app.run_server(debug=True)