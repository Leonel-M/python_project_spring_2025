from data import data
from dash import html,dcc,dash_table
import dash_bootstrap_components as dbc
import plotly.express as px

def histogram(df, x_column, title=None,x_label=None, y_label='Count'):
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
        labels={x_column: x_label or x_column}
    )

    fig.update_layout(
        xaxis_title=x_label or x_column,
        yaxis_title=y_label,
        bargap=0.2
    )

    return fig

def bar_chart(df, x, y,title=None,x_label=None, y_label=None):
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
        labels={x:x_label,y:y_label}
    )
    return fig

def pie(df, values, names,title=None):
    """
    :param df: DataFrame
    :param values: Column name for the size of pie slices
    :param names: Column name for the labels of pie slices
    :param title: Title of the pie chart
    :return:  Plotly pie chart
    """
    fig = px.pie(
        df,
        values=values,
        names=names,
        title=title

    )
    return fig

def header():
    """
    :return:  Dash html.Header component containing the HEADER layout
    """
    return html.Header([
                  html.H1('🛒 Superstore Sales'),
    ], id='id_header')
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/
def avg_shipping():
    return html.Div([
        dbc.Card([
        dbc.CardBody([
            html.H5('Shipping Time Overview'),
            html.P(f'Avg: {data.avg_shipping["mean"]:.2f} days'),
            html.P(f'min: {data.avg_shipping["min"]} days'),
            html.P(f'Median: {data.avg_shipping["50%"]} days'),
            html.P(f'Max: {data.avg_shipping["max"]} days'),
            html.P(f'Std Dev: {data.avg_shipping["std"]:.2f} days'),
            dcc.Graph(figure=histogram(
                data.df,
                'Shipping_Time',
                'Distribution of Shipping Time',
                'Days to Ship',
                'Number of Orders'
            ))
        ])
    ]),

])

def shipping_modes():
    return html.Div([
        dbc.Card([
            html.H5('Average Shipping Time by Ship Mode'),
            dcc.Graph(figure= bar_chart(
                data.ship_modes,
                'Ship_Mode',
                'Shipping_Time',
                'Average Shipping Time by Ship Mode',
                'Ship Mode',
                'Avg. Days ti ship'
                )
            ),
            # https://dash.plotly.com/datatable
            dash_table.DataTable(
                data.ship_modes.to_dict('records'),
                [{"name": i, "id": i} for i in data.ship_modes.columns])
        ])
    ])

def order_by_segment():
    return html.Div([
        dbc.Card([
            html.H5('Order Distribution by Customer Segment'),
            dcc.Graph(figure=pie(
                data.orders_per_segment,
                'count',
                'Segment'),
            ),
            dash_table.DataTable(
                data.orders_per_segment.to_dict('records'),
                [{"name": i, "id": i} for i in data.orders_per_segment.columns])

        ])
    ])

def order_trends():
    pass