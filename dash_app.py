"""
A Minimal Dash App from https://dash.plotly.com/minimal-app

Dash supports adding custom CSS or JavaScript in your apps.
Create a folder named assets in the root of your app directory and include
your CSS and JavaScript files in that folder. Dash automatically serves all the files
that are included in this folder. By default, the URL to request the assets is /assets,
but you can customize this with the assets_url_path argument to dash.Dash.
https://dash.plotly.com/external-resources
"""
from data import data_copy, data
from dash import Dash, callback, Input, Output, html
from components import  header, avg_shipping, shipping_modes, order_by_segment, order_by_location, order_trends
import components
"""
scatter_map configuration https://docs.sisense.com/main/SisenseLinux/scatter-map.htm
"""

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = html.Div([
        components.serve_layout(),
        html.Div(id='output-id')
    ])

# Callback function
@callback(
    Output('avg_shipping', 'children'),
    Output('shipping_modes', 'children'),
    Output('order_by_segment', 'children'),
    Output('order_by_location', 'children'),
    Output('order_trends', 'children'),
    Input('filter-ship', 'value'),  # ID from element, variable
    Input('filter-segment', 'value'),
    Input('filter-state', 'value'),
    Input('filter-month', 'value'),
    Input('filter-week', 'value')

    #State('input-id', 'value')
)
def update_output(ship_value, segment_value, state_value, month_value, week_value):
    filtered = data_copy(data,ship_value, segment_value, state_value, month_value, week_value)
    return components.avg_shipping(filtered), components.shipping_modes(filtered), components.order_by_segment(filtered),components.order_by_location(filtered), components.order_trends(filtered)



if __name__ == '__main__':
    app.run(debug=True)
