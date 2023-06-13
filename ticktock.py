#! /usr/bin/env python

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
import dash
import time

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

collapses = html.Div(
    [
        dbc.Input(
            value="1",
            id="left",
        ),
        dbc.Input(
            value="2",
            id="right",
        )
    ])

app.layout = collapses


@app.callback(
    Output("left", "value"),
    Input("right", "value"),
)
def right_to_left(right):
    val = dash.no_update
    try:
      val = int(right)+1
    except:
      pass
    return val

@app.callback(
    Output("right", "value"),
    Input("left", "value"),
)
def left_to_right(left):
    print(dash.ctx)
    val = dash.no_update
    try:
      val = int(left)+1
    except:
      pass
    return val



if __name__ == '__main__':
    app.run_server(debug=True)
