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
app.layout = html.Section([
    html.div(
        html.H1(children='Global Data'),
        html.H2(
            children=f'Start from 1/22/20 to {dfgbConfirmed.Date.tolist()[-1]}'),
        dcc.Graph(
            id='fstGraph',
            figure=fig,
        )
    ),
    html.div(
        dcc.Dropdown(
            id='demo-dropdown',
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': 'Montreal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            value='NYC'
        ),
    )

])


@app.callback(
    Output(component_id='my-output', component_property='children'),
    [Input(component_id='my-input', component_property='value')]
)
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)


if __name__ == '__main__':
    app.run_server()
