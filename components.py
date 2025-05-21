from data import data
from dash import html,dcc,dash_table
import dash_bootstrap_components as dbc
import plotly.express as px

# Graphics
def histogram(df, x_column,x_label=None, y_label='Count', color=None, title=None):
    """
    Generates a Plotly histogram for a given column in the DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data.
    - x_column (str): Name of the column to be used on the x-axis.
    - title (str, optional): Title of the histogram. Defaults to None.
    - x_label (str, optional): Label for the x-axis. Defaults to the column name.
    - y_label (str, optional): Label for the y-axis. Defaults to "Count".

    Returns:
    - fig (plotly.graph_objs._figure.Figure): A Plotly figure object representing the histogram.
    """
    #https://plotly.com/python/histograms/
    fig = px.histogram(
        df,
        x=x_column,
        title=title,
        labels={x_column: x_label or x_column},
        color_discrete_sequence=[color]
    )

    fig.update_layout(
        xaxis_title=x_label or x_column,
        yaxis_title=y_label,
        bargap=0.2
    )

    return fig
def bar_chart(df, x, y,x_label=None, y_label=None, color= None,title=None):
    """
    :param df: DataFrame
    :param x: Column used for x-axis
    :param y: Column used for y-axis
    :param title: Title of the chart
    :param x_label: Label for x-axis
    :param y_label: Label for y-axis
    :return: Plotly bar chart figure
    """
    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        labels={x:x_label,y:y_label},
        color_discrete_sequence=[color]
    )
    return fig
def pie(df, values, names,title=None, color_sequence=None):
    """
    :param df: DataFrame
    :param values: Column name for the size of pie slices
    :param names: Column name for the labels of pie slices
    :param title: Title of the pie chart
    :return:  Plotly pie chart
    """
    color_sequence = color_sequence[:len(df)] if color_sequence else None
    fig = px.pie(
        df,
        values=values,
        names=names,
        title=title,
        color_discrete_sequence=color_sequence

    )
    return fig
def us_state_map(df,locations,color, title=None,locationmode='USA-states', scope='usa', color_continuous_scale='Blues'):
    """
    Choropleth map of USA by State
    :type color: object
    :param df: DataFrame
    :param locations: Column with abbreviations
    :param locationmode: Location reference
    :param color: Column for scale
    :param scope: Geographic scope
    :param title: Tile of the map
    :param color_continuous_scale:
    :return: Choropleth map figure
    """
    fig = px.choropleth(
        df,
        locations= locations,
        locationmode= locationmode,
        color= color,
        scope= scope,
        title= title,
        color_continuous_scale=color_continuous_scale
    )
    return fig

# Filter bar
"""
    Callbacks are Dash functions to make dynamic changes to the application.
    https://dash.plotly.com/sharing-data-between-callbacks
"""
def filter_bar():
    """
    :return: Dash html.Div component containing filters

    Unique  values in each Dropdown
    https://community.plotly.com/t/how-to-populate-a-dropdown-from-unique-values-in-a-pandas-data-frame/5543/2
    """
    return html.Div([
        html.Div([
            dcc.Dropdown(
                id='filter-ship',
                options=[{'label': i, 'value': i} for i in data.ship_modes['Ship_Mode'].unique()],
                multi=True, placeholder='Filter by Ship Mode...',
                value= None
                ),
            dcc.Dropdown(
                id='filter-segment',
                options=[{'label': i, 'value': i} for i in data.orders_per_segment['Segment'].unique()],
                multi=True, placeholder='Filter by Customer Segment...',
                value= None
            ),
            dcc.Dropdown(
                id='filter-state',
                options=[{'label': i, 'value': i} for i in data.orders_per_state['State'].unique()],
                multi=True, placeholder='Filter by State...',
                value= None
            ),
            dcc.Dropdown(
                id='filter-month',
                options=[{'label': i, 'value': i} for i in data.orders_per_month['Month'].unique()],
                multi=True, placeholder='Filter by Month...',
                value= None
            ),
            dcc.Dropdown(
                id='filter-week',
                options=[{'label': i, 'value': i} for i in data.orders_per_week['Weekday'].unique()],
                multi=True, placeholder='Filter by Weekday...',
                value= None
            )

        ], className='filter-content')
    ], className='component-section')

# Dash components
def header():
    """
    :return:  Dash html.Header component containing the HEADER layout
    """
    return html.Header([
                  html.H1('🛒 Superstore Sales'),
    ], id='id_header')
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/
def avg_shipping():
    """
    :return: Dash html.Div component containing shipping orders
    """
    return html.Div([
        html.Div([
            html.H3('Shipping Time Overview', className='section-title'),
            html.Div([
                html.P(f'Avg: {data.avg_shipping["mean"]:.2f} days'),
                html.P(f'min: {data.avg_shipping["min"]} days'),
                html.P(f'Median: {data.avg_shipping["50%"]} days'),
                html.P(f'Max: {data.avg_shipping["max"]} days'),
                html.P(f'Std Dev: {data.avg_shipping["std"]:.2f} days')
            ], className='section-summary'),

            dcc.Graph(figure=histogram(
                data.df,
                'Shipping_Time',
                'Days to Ship',
                'Number of Orders',
                'rgb(244, 161, 0)',
                'Distribution of Shipping Time'
            ))
        ], className='card-content'),
    ], className='component-section')

def shipping_modes():
    """
    :return: Dash html.Div component containing Ship Modes
    """
    return html.Div([
        html.Div([
            html.H3('Average Shipping Time by Ship Mode', className="section-title"),
            dcc.Graph(figure= bar_chart(
                data.ship_modes,
                'Ship_Mode',
                'Shipping_Time',
                'Ship Mode',
                'Avg. Days per ship',
                'rgb(255, 65, 58)'
                )
            ),
            # https://dash.plotly.com/datatable
            dash_table.DataTable(
                data.ship_modes.to_dict('records'),
                [{"name": i, "id": i} for i in data.ship_modes.columns],
            style_cell={'textAlign':'left'}
            )

        ], className='card-content')
    ], className='component-section')

def order_by_segment():
    """
    :return: Dash html.Div component containing Customer Segments
    """
    return html.Div([
        html.Div([
            html.H3('Order Distribution by Customer Segment', className="section-title"),
            dcc.Graph(figure=pie(
                data.orders_per_segment,
                'count',
                'Segment',
                color_sequence=["#28f6a7", "#00ac69", "#275e49", "#2d2d2d"]),

            ),
            dash_table.DataTable(
                data.orders_per_segment.to_dict('records'),
                [{"name": i, "id": i} for i in data.orders_per_segment.columns],
            style_cell={'textAlign':'left'}
            )

        ],className="card-content")
    ], className="component-section")

def order_by_location():
    """
    :return: Dash html.Div component containing Order Volume Locations
    """
    return html.Div([
        html.Div([
            html.H3('Order volume by location',className="section-title"),
            dcc.Graph(figure=us_state_map(
                data.orders_per_state,
                'State_Code',
                'Order_Count',
            )),
            dash_table.DataTable(
                data.orders_per_city.to_dict('records'),
                [{"name": i, "id": i} for i in data.orders_per_city.columns],
                style_table={'height': '200px',
                             'overflowY': 'auto'},
                style_cell={'textAlign': 'left'}
        )

        ], className="card-content")
    ], className="component-section")

def order_trends():
    """
    :return: Dash html.Div component containing monthly and Weekly order patterns
    """
    return  html.Div([
                html.Div([
                    html.H3('Monthly and Weekly Order Patterns', className="section-title"),
                    dcc.Graph(figure=bar_chart(
                        data.orders_per_month,
                        'Month',
                        'Order_Count',
                        'Month',
                        'Orders per Month',
                        'rgb(153, 51, 255)',
                        'Orders per Month'
                    )),
                    dcc.Graph(figure=bar_chart(
                        data.orders_per_week,
                        'Weekday',
                        'Order_Count',
                        'Weekday',
                        'Orders per Weekday',
                        'rgb(153, 51, 255)',
                        'Orders per Weekday'
                    ))
                ], className="card-content")

        ], className='component-section')