""" Dash app for wifi device control"""

from dash import Dash, html, dcc

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

])

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True)