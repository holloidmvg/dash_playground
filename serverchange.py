#! /usr/bin/env python

import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, State, html
import dash
import time

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server_id = time.time_ns()
print(server_id)
gui_state_store = dcc.Store(id="gui_state_store", data={'server_id' : server_id, 'delay' : None})

collapses = html.Div(
    [
        html.Div(id='sink1', style={'display':'none'}),
        dcc.Interval(id="gui_interval", interval=100, n_intervals=0),
        dcc.Location(id='url', refresh=True),
        gui_state_store,
        html.Div(id="status",
                 children="All is well",
                 style={"white-space": "pre-wrap"}
        ),
        dbc.Input(
            value="1",
            id="left",
        ),
        dbc.Input(
            value="2",
            id="right",
        ),
        dbc.Input(
            value="3",
            id="right2",
        )
    ])

app.layout = collapses

@app.callback(output=[Output('status', 'children'),
                      Output('gui_state_store', 'data'),
                      Output('url', 'href')],
              inputs=[Input('gui_interval', 'n_intervals'),
                      State('gui_state_store', 'data')])
def timer_triggered(dummy, data):
  time.sleep(1)
  global server_id
  print(f'server_ids {server_id} / {data["server_id"]}')
  msg = 'no message'
  href = dash.no_update
  if data['server_id'] == server_id:
    data['delay'] = None
  else:
    if data['delay'] is not None:
      elapsed = time.time()-data['delay']
      msg = f'elapsed = {elapsed}'
      print(msg)
      if elapsed>5:
        href='/'
        print(f'{data["server_id"]} -> {server_id}')
        data['server_id'] = server_id
        pass
    else:
      print('initialising delay')
      data['delay'] = time.time()
  return (msg, data, href)

"""
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
"""


if __name__ == '__main__':
    #app.run_server(debug=False)
    from waitress import serve
    serve(app.server, host="0.0.0.0", port=8050, threads=100)
