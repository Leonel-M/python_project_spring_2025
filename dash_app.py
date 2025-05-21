"""
A Minimal Dash App from https://dash.plotly.com/minimal-app

Dash supports adding custom CSS or JavaScript in your apps.
Create a folder named assets in the root of your app directory and include
your CSS and JavaScript files in that folder. Dash automatically serves all the files
that are included in this folder. By default, the URL to request the assets is /assets,
but you can customize this with the assets_url_path argument to dash.Dash.
https://dash.plotly.com/external-resources
"""

from dash import Dash, html
from components import  header, avg_shipping, shipping_modes, order_by_segment, order_by_location, order_trends, filter_bar

"""
scatter_map configuration https://docs.sisense.com/main/SisenseLinux/scatter-map.htm
"""

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = html.Div([
    header(),

    html.Hr(),

    #
    html.Div([
        html.Div(filter_bar(), className='card-full', id='filter-bar'),
    ], className='row'),

    # Shipping overview and modes
    html.Div([
        html.Div(avg_shipping(), className='card-half', id='avg_shipping'),
        html.Div(shipping_modes(), className='card-half', id='shipping_modes'),
    ], className='row'),

    # Segment and Location
    html.Div([
        html.Div(order_by_segment(), className='card-half', id='order_by_segment'),
        html.Div(order_by_location(), className='card-half', id='order_by_location'),
    ], className='row'),

    # Trends
    html.Div([
        html.Div(order_trends(), className='card-full', id='order_trends'),
    ], className='row'),

],id='app')


if __name__ == '__main__':
    app.run(debug=True)
