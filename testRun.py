import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

app = dash.Dash()

app.layout = html.Div([
    html.Div([
        html.H1('Title should be here')
    ], className='title'),
    html.Div([
        html.Div([
            html.H2('graphs will be here')
        ], className='graphContainer'),
        html.Div([
            html.H2('Global data will be here')
        ], className='globalDataContainer')
    ], className='lowerPartContainer')
], className='biggestContainer')


if __name__ == '__main__':
    app.run_server(debug=False)
