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

# ------- app start from here -------

app = dash.Dash()

app.layout = html.Div(
    [
        html.Div(
            [html.H1("COVID-19 Dashboard")],
            className="titleContainer",
            style={"border": "2px black solid"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H2("National Data")], className="nationalData"
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Dropdown(
                                                    id="countryDropdown",
                                                    options=optCountries,
                                                )
                                            ],
                                            className="dropdown",
                                        ),
                                        html.Div(
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
                                                    labelStyle={
                                                        "display": "inline-block"
                                                    },
                                                )
                                            ],
                                            className="radioItems",
                                        ),
                                    ],
                                    className="functions",
                                ),
                            ],
                            className="graphHeader",
                            style={"border": "2px red solid"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [dcc.Graph(id="chosenGraph")], className="graph"
                                ),
                            ],
                            className="graphContainer",
                        ),
                    ],
                    className="leftPart",
                ),
                html.Div([html.H2("Here are global data")], className="rightPart"),
            ],
            className="lowerPartContainer",
        ),
    ],
    className="biggestContainer",
)


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


# def update_figure1(countryDropdown, graphSelection):
#     barColor = "rgb(8,48,107)"
#     if graphSelection == "TTL":

#         fig = make_subplots(rows=1)

#         fig.add_bar(
#             x=dfConfirmed["Date"],
#             y=dfConfirmed[countryDropdown],
#             marker_color="rgb(8,48,107)",
#             marker_line_color="rgb(8,48,107)",
#             marker_line_width=1.5,
#             opacity=1,
#             name="Confirmed",
#         )
#         fig.add_bar(
#             x=dfRecovered["Date"],
#             y=dfRecovered[countryDropdown],
#             marker_color="rgb(102,255,178)",
#             marker_line_color="rgb(102,255,178)",
#             marker_line_width=1.5,
#             opacity=1,
#             name="Recovered",
#         )
#         fig.add_bar(
#             x=dfDeaths["Date"],
#             y=dfDeaths[countryDropdown],
#             marker_color="rgb(255,102,102)",
#             marker_line_color="rgb(255,102,102)",
#             marker_line_width=1.5,
#             opacity=1,
#             name="Deaths",
#         )

#         fig.update_layout(title_text="Total Confirmed/Recovered/Deaths Cases")

#         return fig
#     elif graphSelection == "DNC":
#         fig2 = px.bar(dailyGlobalNewCases, x="Date", y=countryDropdown)
#         fig2.update_traces(marker_color=barColor, marker_line_color=barColor, opacity=1)
#         fig2.update_layout(title_text="Daily New Cases")

#         return fig2

#     elif graphSelection == "ATC":
#         fig3 = px.bar(dfActive, x="Date", y=countryDropdown)
#         fig3.update_traces(marker_color=barColor, marker_line_color=barColor, opacity=1)
#         fig3.update_layout(title_text="Active Cases")

#         return fig3


if __name__ == "__main__":
    app.run_server(debug=False)