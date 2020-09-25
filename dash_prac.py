import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# dfConfirmed = pd.read_csv('confirmed.csv').drop('Unnamed: 0', axis=1)
# dfdeaths = pd.read_csv('deaths.csv').drop('Unnamed: 0', axis=1)
# dfrecovered = pd.read_csv('recovered.csv').drop('Unnamed: 0', axis=1)
# print(dfConfirmed.shape)

dfgbConfirmed = pd.read_csv('globalTtl.csv').drop('Unnamed: 0', axis=1)


fig = px.scatter(dfgbConfirmed, x='Date', y='Global Total')

app = dash.Dash()
app.layout = html.Div([
    html.H1(children='Global Data',
            ),
    dcc.Graph(
        id='fstGraph',
        figure=fig,

    )
])

if __name__ == '__main__':
    app.run_server()
