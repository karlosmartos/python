import dash
from dash.dependencies import Input, Output
from dash import dcc, html
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

app = dash.Dash(__name__)
server = app.server

df = pd.DataFrame({"System": ["Python backend", "Assembly backend"], "Lines of code": [3183, 38], "Number of devs in my timezone capable of doing the coding": [4236, 3]})

app.layout = dbc.Container([
    html.H1("Python or Assembly?", style={'text-align': 'center'}),
    dcc.Dropdown(["Python backend", "Assembly backend"], id="slct_source", value="Python backend", style={"width": "90%"}),
    dcc.Graph(id='varieties_fig', figure={}), 
])

@app.callback(Output(component_id='varieties_fig', component_property='figure'),Input(component_id='slct_source', component_property='value'))
def update_graph(option_slctd):

    dff = df.copy()
    dff =dff[dff['System'] == option_slctd]
    fig = px.bar(dff, y=['Lines of code', 'Number of devs in my timezone capable of doing the coding'], x='System', barmode='group')
    return fig

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
