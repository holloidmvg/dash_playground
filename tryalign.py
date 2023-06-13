#! /usr/bin/env python

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
import dash
import dash_daq as daq
import time

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


def right(text):
  return dbc.Col(dbc.Row(children=text, justify='end'), width=True)

def left(text):
  return dbc.Col(dbc.Row(children=text, justify='start'), width=True)


collapses = html.Div([
    dbc.Row([
      right("left"),
      dbc.Col(daq.ToggleSwitch(label="Mode"), width=1),
      left("right")
    ]),
    dbc.Row(dbc.Col("a xvery, very, long winded text", width=False))])

app.layout = collapses




if __name__ == '__main__':
    app.run_server(debug=True)
