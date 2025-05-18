from data import data
from dash import html,dcc

def header():
    """
    :return:  Dash html.Header component containing the HEADER layout
    """
    return html.Header([
                  html.H1('🛒 Superstore Sales'),
    ], id='id_header')