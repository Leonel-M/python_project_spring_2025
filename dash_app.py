"""
A Minimal Dash App from https://dash.plotly.com/minimal-app

Dash supports adding custom CSS or JavaScript in your apps.
Create a folder named assets in the root of your app directory and include
your CSS and JavaScript files in that folder. Dash automatically serves all the files
that are included in this folder. By default, the URL to request the assets is /assets,
but you can customize this with the assets_url_path argument to dash.Dash.
https://dash.plotly.com/external-resources
"""

from dash import Dash, html, Input, Output
from data import filter_df, data
from components import  header, avg_shipping, shipping_modes, order_by_segment, order_by_location, order_trends, filter_bar

"""
scatter_map configuration https://docs.sisense.com/main/SisenseLinux/scatter-map.htm
"""

app = Dash()

# ------ Dashboard with the components
app.layout = html.Div([
    header(),

    html.Hr(),

    #
    html.Div([
        html.Div([filter_bar()], className='card-full', id='filter-bar'),
    ], className='row'),

    # Shipping overview and modes
    html.Div([
        html.Div([avg_shipping()], className='card-half', id='avg_shipping'),
        html.Div([shipping_modes()], className='card-half', id='shipping_modes'),
    ], className='row'),

    # Segment and Location
    html.Div([
        html.Div([order_by_segment()], className='card-half', id='order_by_segment'),
        html.Div([order_by_location()], className='card-half', id='order_by_location'),
    ], className='row'),

    # Trends
    html.Div([
        html.Div([order_trends()], className='card-full', id='order_trends'),
    ], className='row'),

],id='app')

# ------ Callback to filter and update data
@app.callback(
    [Output('avg_shipping', 'children'),
        Output('shipping_modes', 'children'),
        Output('order_by_segment', 'children'),
        Output('order_by_location', 'children'),
        Output('order_trends', 'children')
     ],
    [
        Input('filter-ship', 'value'),  # argument: ship
        Input('filter-segment', 'value'),  # argument: segment
        Input('filter-state', 'value'),  # argument: state
        Input('filter-month', 'value'),  # argument: month
        Input('filter-week', 'value'),  # argument: week
    ]
)
def update_data(ship, segment, state, month, week):
    try:
        new_object = filter_df(data, ship, segment, state, month, week)
        return (
            avg_shipping(new_object),
            shipping_modes(new_object),
            order_by_segment(new_object),
            order_by_location(new_object),
            order_trends(new_object)
        )
    except Exception as e:
        import traceback
        print("❌ Callback error:")
        traceback.print_exc()
        return [html.Div(f"Error: {str(e)}")] * 5


if __name__ == '__main__':
    app.run(debug=True)
