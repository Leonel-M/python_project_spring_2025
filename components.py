from data import data
from dash import html,dcc
import dash_bootstrap_components as dbc

def header():
    """
    :return:  Dash html.Header component containing the HEADER layout
    """
    return html.Header([
                  html.H1('🛒 Superstore Sales'),
    ], id='id_header')

# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/
def avg_shipping():
    return dbc.Card([
        dbc.CardBody([
            html.H5('Shipping Time Overview'),
            html.P(f'Avg: {data.avg_shipping["mean"]} days'),
            html.P(f'min: {data.avg_shipping["min"]} days'),
            html.P(f'Median: {data.avg_shipping["50%"]} days'),
            html.P(f'Max: {data.avg_shipping["max"]} days'),
            html.P(f'Std Dev: {data.avg_shipping["std"]} days')

        ])
    ])
