""" Dash app for wifi device control"""

from dash import Dash, html, dcc, Input, Output
from kasa import Discover, smartstrip
import asyncio
import time
import schedule
import sys

from devices import StripPort
from scheduling import run_continuously

IP_ADDRESS = sys.argv[1]
strip = asyncio.run(Discover.discover_single(IP_ADDRESS))
port_map = {}
for index, child in enumerate(strip.children):
    port_map[child.alias] = StripPort(IP_ADDRESS, index)

app = Dash(__name__)

checkbox_list = list(port_map.keys())

stop_schedule = None

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
    html.Label('Checkboxes'),
    dcc.Checklist(
        checkbox_list,
        [child.alias for child in strip.children if child.is_on],
        id='on_off',
    ),
    html.Div(id='my-output'),
    dcc.Input(id="charge_time", type="text", placeholder="", debounce=True),
    html.Div(id='charge_time_output'),
])

def dehumid_off_car_on():
    port_map['Dehumidifier'].turn_off()
    port_map['Car'].turn_on()

@app.callback(
    Output("charge_time_output", "children"),
    Input("charge_time", "value")
)
def set_car_schedule(start_time: str):
    if start_time is None:
        return ""
    print(f"Start Time: |{start_time}|")
    global stop_schedule
    if stop_schedule is not None:
        stop_schedule.set()
    schedule.clear()
    schedule.every().day.at(start_time).do(dehumid_off_car_on)
    stop_schedule = run_continuously(interval=5)
    return f"Scheduled car on at {start_time}"

@app.callback(
    Output("my-output", "children"),
    Input("on_off", "value")
)
def set_state(checkboxes):
    result = 'Turned on: '
    for box in checkboxes:
        port_map[box].turn_on()
        result += box
    result += "Turned off: "
    for cb in checkbox_list:
        if cb not in checkboxes:
            port_map[cb].turn_off()
            result += cb
    return result

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True)