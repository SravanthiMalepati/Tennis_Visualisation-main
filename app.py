import os
import pandas as pd
from dash import Dash, callback_context, no_update
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plot_final_new as plot

path = "./data/sample_tennis_data_table.csv"
df = pd.read_csv(path)

app = Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='graph'),
        dcc.Location(id='url',refresh=False)
        
    ]
)
@app.callback(Output('graph', 'figure'),
              [Input('url', 'pathname')])
def display_page(pathname):
    df = pd.read_csv(f'./data{pathname}.csv')
    fig = plot.plotly(df)
    return fig
if __name__ == "__main__":
    app.run_server(host='127.0.0.1',debug=True)
