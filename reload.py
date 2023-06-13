#! /usr/bin/env python

import random

import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, State, html
from dash.exceptions import PreventUpdate
import dash
import time


# GUI_STATE holds more then just bidirectional items
class GuiState(dict):
  pass

class GuiControlID:
  def __init__(self, name, property_, value, id_):
    self.__name = name
    self.__property = property_
    self.__value = value
    if id_ is None:
      id_ = 'id_'+name.lower()
    self.__id = id_
    self.__id_used = False
  @property
  def id(self):
    self.__id_used = True
    return self.__id


  def __str__(self):
    return self.__name

class GuiControls:
  def __init__(self):
    self.controls = {}
    self.output_names = []
    self.output = None
  def new(self, name, property_, value, id_=None):
    gcid = GuiControlID(name, property_, value, id_)
    globals()[name] = gcid
    self.controls[gcid._GuiControlID__id] = gcid
    self.output_names.append(name)
  def create_gui_state(self):
    gui_state = GuiState( ( (el, el._GuiControlID__value) for el in self.controls.values() ) )
    return gui_state
  def from_id(self, id_):
    return self.controls[id_]
  def invoke_on_all_for_decorator_dict(self, func):
    ret = {}
    for el in self.controls.values():
      if el._GuiControlID__id_used:
        ret[str(el)] = func(el.id, el._GuiControlID__property)
    return ret

controls = GuiControls()
controls.new('PUMP_DURATION', 'value', 2)
controls.new('SAMPLE_FRACTION', 'value', .2)
GUI_STATE = controls.create_gui_state()

# add other stuff to GUI_STATE
RED_TARGET = "RED_TARGET"  # red channel intensity target
GUI_STATE[RED_TARGET] = 40

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

layout = html.Div(
    [   html.Div(id='sink1', style={'display':'none'}),
        dcc.Interval(id="gui_interval", interval=1 * 1000, n_intervals=0),
        dbc.Input(
            value=GUI_STATE[PUMP_DURATION],
            id=PUMP_DURATION.id,
            debounce=True
        ),
        dbc.Input(
            value=GUI_STATE[SAMPLE_FRACTION],
            id=SAMPLE_FRACTION.id,
            debounce=True
        )
    ])

@app.callback(output=[Output('sink1','style')],
              inputs=[controls.invoke_on_all_for_decorator_dict(Input)])
def deal_with_input(dummy):
  if len(dash.callback_context.triggered) > 1:
    print('multi input ignored')
    raise PreventUpdate
  input_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
  if not input_id:
    raise PreventUpdate
  value = dash.callback_context.triggered[0]['value']
  print(f'INVOKED {controls.from_id(input_id)}({input_id}) -> {value}')
  raise PreventUpdate

@app.callback(output=controls.invoke_on_all_for_decorator_dict(Output),
              inputs=[Input('gui_interval', 'n_intervals')])
def timer_triggered(dummy):
  dcc.Location.refresh(True)
  # Simulate an update from the device (as dict rather than list)
  update_from_device = {str(PUMP_DURATION) : 20*random.random(),
                        'something_else' : 42,
                        str(SAMPLE_FRACTION) : random.random()}
  #output = controls.get_output_template(dash.no_update)
  output = {}
  for key in controls.output_names:
    output[key] = update_from_device.get(key, dash.no_update)
  return output

app.layout = layout


if __name__ == '__main__':
    app.run_server(debug=True)
