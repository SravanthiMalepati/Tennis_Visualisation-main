import os
import pandas as pd
from dash import Dash, callback_context, no_update
from dash.dependencies import Input, Output
#from dash_table import DataTable
import dash_core_components as dcc
import dash_html_components as html
import plot_final_new as plot

path = "./data/sample_tennis_data_table.csv"
df = pd.read_csv(path)

app = Dash(__name__)
app.layout = html.Div(
    [
        #html.H1('match details', style={'backgroundColor':'rgb(0,0,0)'}),
        dcc.Graph(id='graph'),
        dcc.Location(id='url',refresh=False)
        
        # DataTable(
        #     id="table",
        #     columns=[{"name": i, "id": i} for i in df.columns],
        #     data=df.to_dict("records"),
        #     export_format="csv",
        # )
    ]
)
@app.callback(Output('graph', 'figure'),
              [Input('url', 'pathname')])
def display_page(pathname):
    df = pd.read_csv(f'./data{pathname}.csv')

    #return df.to_dict("records"), [{"name": i, "id": i} for i in df.columns]
    #print('sravanthi')
    fig = plot.plotly(df)
    return fig



if __name__ == "__main__":
    app.run_server(host='127.0.0.1',debug=True)
    #app.run_server(host='127.0.0.1', port=8080, debug=True)