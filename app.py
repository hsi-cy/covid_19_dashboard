import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

dfConfirmed = pd.read_csv('confirmed.csv').drop('Unnamed: 0', axis=1)
listOfCountries = list(dfConfirmed.columns[1:])
optCountries = []
for country in listOfCountries:
    dic = {'label': country, 'value': country}
    optCountries.append(dic)
dfDeaths = pd.read_csv('deaths.csv').drop('Unnamed: 0', axis=1)


def dfForCountryGraph(countryName):
    """create a dataframe for the countryGraph"""
    plotDf = pd.DataFrame()
    plotDf['Date'] = dfConfirmed['Date']
    plotDf['Confirmed'] = dfConfirmed[countryName]
    plotDf['Deaths'] = dfDeaths[countryName]
    return plotDf

# dfrecovered = pd.read_csv('recovered.csv').drop('Unnamed: 0', axis=1)
# print(dfConfirmed.shape)


dfgbConfirmed = pd.read_csv('globalTtl.csv').drop('Unnamed: 0', axis=1)


app = dash.Dash()
app.layout = html.Div([
    html.H1(f'Global Total Cases: {dfgbConfirmed['globalTotal'][-1]}')
]), html.Div([
    dcc.Dropdown(
        id='countryDropdown',
        options=optCountries,
        value='Select a country.'
    ),
    dcc.Graph(
        id='singleCountryGraph',
    )])


@app.callback(
    Output(component_id='singleCountryGraph', component_property='figure'),
    [Input(component_id='countryDropdown', component_property='value')]
)
def update_figure(selected_country):
    df = dfForCountryGraph(selected_country)
    fig = make_subplots(rows=1)

    fig.add_bar(x=df['Date'], y=df['Confirmed'], marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                marker_line_width=1.5, opacity=1, name='Confirmed')
    fig.add_bar(x=df['Date'], y=df['Deaths'], marker_color='rgb(255,102,102)', marker_line_color='rgb(255,102,102)',
                marker_line_width=1.5, opacity=1, name='Deaths')

    # fig = px.bar(dfForCountryGraph(selected_country),
    #              x='Date', y=selected_country)

    # fig.update_layout(transition_duration=500)
    # fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
    #                   marker_line_width=1.5, opacity=0.6)

    return fig


if __name__ == '__main__':
    app.run_server()
