import dash
import dash_bootstrap_components as dbc
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
dailyGlobalNewCases = pd.read_csv('dailyGlobalNewCases.csv')


def dfForCountryGraph(countryName):
    """create a dataframe for the countryGraph"""
    plotDf = pd.DataFrame()
    plotDf['Date'] = dfConfirmed['Date']
    plotDf['Confirmed'] = dfConfirmed[countryName]
    plotDf['Deaths'] = dfDeaths[countryName]
    return plotDf


dfActive = pd.read_csv('active.csv').drop('Unnamed: 0', axis=1)
dfRecovered = pd.read_csv('recovered.csv').drop('Unnamed: 0', axis=1)

dfgbConfirmed = pd.read_csv('globalTtl.csv').drop('Unnamed: 0', axis=1)

# ------- app start from here -------

app = dash.Dash()

app.layout = html.Div([
    html.Div([
        html.H1('COVID-19 Dashboard', id='title')
    ]),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='countryDropdown',
                options=optCountries,
            ),
            dcc.Graph(
                id='confirmedGraph',
            ),
            dcc.Graph(
                id='dailyNewGraph',
            ),
            dcc.Graph(
                id='activeGraph',
            )], className='container')],
        # html.Div([

        # ])
    )

])


@ app.callback(
    [Output(component_id='confirmedGraph', component_property='figure'),
     Output(component_id='dailyNewGraph', component_property='figure'),
     Output(component_id='activeGraph', component_property='figure')],
    [Input(component_id='countryDropdown', component_property='value')]
)
def update_figure1(selected_country):
    df = dfForCountryGraph(selected_country)
    fig = make_subplots(rows=1)

    fig.add_bar(x=df['Date'], y=df['Confirmed'], marker_color='rgb(8,48,107)', marker_line_color='rgb(8,48,107)',
                marker_line_width=1.5, opacity=1, name='Confirmed')
    fig.add_bar(x=dfRecovered['Date'], y=dfRecovered[selected_country], marker_color='rgb(102,255,178)', marker_line_color='rgb(102,255,178)',
                marker_line_width=1.5, opacity=1, name='Recovered')
    fig.add_bar(x=df['Date'], y=df['Deaths'], marker_color='rgb(255,102,102)', marker_line_color='rgb(255,102,102)',
                marker_line_width=1.5, opacity=1, name='Deaths')

    fig.update_layout(title_text='Total Confirmed/Recovered/Deaths Cases')

    # fig = px.bar(dfForCountryGraph(selected_country),
    #              x='Date', y=selected_country)

    # fig.update_layout(transition_duration=500)
    # fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
    #                   marker_line_width=1.5, opacity=0.6)
    bar_color = 'rgb(8,48,107)'
    df2 = dailyGlobalNewCases.copy()
    fig2 = px.bar(df2, x='Date', y=selected_country)
    fig2.update_traces(marker_color=bar_color,
                       marker_line_color=bar_color, opacity=1)
    fig2.update_layout(title_text='Daily New Cases')

    df3 = dfActive.copy()
    fig3 = px.bar(df3, x='Date', y=selected_country)
    fig3.update_traces(marker_color=bar_color,
                       marker_line_color=bar_color, opacity=1)
    fig3.update_layout(title_text='Active Cases')

    return fig, fig2, fig3


# def update_figure2(selected_country):
#     df2 = dailyGlobalNewCases.copy()
#     fig2 = px.bar(df2, x='Date', y=selected_country)
#     fig2.update_layout(title_text='Daily New Cases')

#     return fig2


# def update_figure3(selected_country):
#     df3 = dfActive.copy()
#     fig3 = px.bar(df3, x='Date', y=selected_country)
#     fig3.update_layout(title_text='Active Cases')

#     return fig3


if __name__ == '__main__':
    app.run_server(debug=True)
