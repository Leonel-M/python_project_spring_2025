"""
components.py

Defines layout and visual components for the Superstore dashboard.
Includes dropdown filters, date pickers, and interactive charts using Plotly.
"""

from data import data
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px


# Graphics
def histogram(df, x_column, x_label=None, y_label="Count", color=None, title=None):
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
    # https://plotly.com/python/histograms/
    fig = px.histogram(
        df,
        x=x_column,
        title=title,
        labels={x_column: x_label or x_column},
        color_discrete_sequence=[color],
    )

    fig.update_layout(xaxis_title=x_label or x_column, yaxis_title=y_label, bargap=0.2)

    return fig


def bar_chart(df, x, y, x_label=None, y_label=None, color=None, title=None):
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
        labels={x: x_label, y: y_label},
        color_discrete_sequence=[color],
    )
    return fig


def pie(df, values, names, title=None, color_sequence=None):
    """
    :param df: DataFrame
    :param values: Column name for the size of pie slices
    :param names: Column name for the labels of pie slices
    :param title: Title of the pie chart
    :return:  Plotly pie chart
    """
    color_sequence = color_sequence[: len(df)] if color_sequence else None
    fig = px.pie(
        df,
        values=values,
        names=names,
        title=title,
        color_discrete_sequence=color_sequence,
    )
    return fig


def us_state_map(
    df,
    locations,
    color,
    title=None,
    locationmode="USA-states",
    scope="usa",
    color_continuous_scale="Blues",
):
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
        locations=locations,
        locationmode=locationmode,
        color=color,
        scope=scope,
        title=title,
        color_continuous_scale=color_continuous_scale,
    )
    return fig


# Dash components
def header():
    """
    :return:  Dash html.Header component containing the HEADER layout
    """
    return html.Header(
        [
            html.Img(src="assets/icon.png", id="icon"),
            html.H1("Superstore Sales"),
        ],
        id="id_header",
    )


def avg_shipping(obj):
    """
    :return: Dash html.Div component containing shipping orders
    """
    return html.Div(
        [
            html.Div(
                [
                    html.H3("Shipping Time Overview", className="section-title"),
                    html.Div(
                        [
                            html.P(f'Avg: {obj.avg_shipping_info["mean"]:.2f} days'),
                            html.P(f'min: {obj.avg_shipping_info["min"]} days'),
                            html.P(f'Median: {obj.avg_shipping_info["50%"]} days'),
                            html.P(f'Max: {obj.avg_shipping_info["max"]} days'),
                            html.P(f'Std Dev: {obj.avg_shipping_info["std"]:.2f} days'),
                        ],
                        className="section-summary",
                    ),
                    dcc.Graph(
                        figure=histogram(
                            obj.df,
                            "Shipping_Time",
                            "Days to Ship",
                            "Number of Orders",
                            "rgb(244, 161, 0)",
                            "Distribution of Shipping Time",
                        )
                    ),
                ],
                className="card-content",
            ),
        ],
        className="component-section",
    )


def shipping_modes(obj):
    """
    :return: Dash html.Div component containing Ship Modes
    """
    return html.Div(
        [
            html.Div(
                [
                    html.H3(
                        "Average Shipping Time by Ship Mode", className="section-title"
                    ),
                    dcc.Graph(
                        figure=bar_chart(
                            obj.ship_modes_info,
                            "Ship_Mode",
                            "Shipping_Time",
                            "Ship Mode",
                            "Avg. Days per ship",
                            "rgb(255, 65, 58)",
                        )
                    ),
                    # https://dash.plotly.com/datatable
                    dash_table.DataTable(
                        obj.ship_modes_info.to_dict("records"),
                        [{"name": i, "id": i} for i in data.ship_modes_info.columns],
                        style_cell={"textAlign": "left"},
                    ),
                ],
                className="card-content",
            )
        ],
        className="component-section",
    )


def order_by_segment(obj):
    """
    :return: Dash html.Div component containing Customer Segments
    """
    return html.Div(
        [
            html.Div(
                [
                    html.H3(
                        "Order Distribution by Customer Segment",
                        className="section-title",
                    ),
                    dcc.Graph(
                        figure=pie(
                            obj.orders_per_segment_info,
                            "count",
                            "Segment",
                            color_sequence=["#28f6a7", "#00ac69", "#275e49", "#2d2d2d"],
                        ),
                    ),
                    dash_table.DataTable(
                        obj.orders_per_segment_info.to_dict("records"),
                        [
                            {"name": i, "id": i}
                            for i in obj.orders_per_segment_info.columns
                        ],
                        style_cell={"textAlign": "left"},
                    ),
                ],
                className="card-content",
            )
        ],
        className="component-section",
    )


def order_by_location(obj):
    """
    :return: Dash html.Div component containing Order Volume Locations
    """
    return html.Div(
        [
            html.Div(
                [
                    html.H3("Order volume by location", className="section-title"),
                    dcc.Graph(
                        figure=us_state_map(
                            obj.orders_per_state_info,
                            "State_Code",
                            "Order_Count",
                        )
                    ),
                    dash_table.DataTable(
                        obj.orders_per_city_info.to_dict("records"),
                        [
                            {"name": i, "id": i}
                            for i in obj.orders_per_city_info.columns
                        ],
                        style_table={"height": "200px", "overflowY": "auto"},
                        style_cell={"textAlign": "left"},
                    ),
                ],
                className="card-content",
            )
        ],
        className="component-section",
    )


def order_trends(obj):
    """
    :return: Dash html.Div component containing monthly and Weekly order patterns
    """
    return html.Div(
        [
            html.Div(
                [
                    html.H3(
                        "Monthly and Weekly Order Patterns", className="section-title"
                    ),
                    dcc.Graph(
                        figure=bar_chart(
                            obj.orders_per_month_info,
                            "Month",
                            "Order_Count",
                            "Month",
                            "Orders per Month",
                            "rgb(153, 51, 255)",
                            "Orders per Month",
                        )
                    ),
                    dcc.Graph(
                        figure=bar_chart(
                            obj.orders_per_week_info,
                            "Weekday",
                            "Order_Count",
                            "Weekday",
                            "Orders per Weekday",
                            "rgb(153, 51, 255)",
                            "Orders per Weekday",
                        )
                    ),
                ],
                className="card-content",
            )
        ],
        className="component-section",
    )


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
    return html.Div(
        [
            html.Div(
                [
                    dcc.Dropdown(
                        id="filter-ship",
                        className="dropdown",
                        options=[
                            {"label": i, "value": i}
                            for i in data.ship_modes_info["Ship_Mode"].unique()
                        ],
                        multi=True,
                        placeholder="Filter by Ship Mode...",
                        value=None,
                    ),
                    dcc.Dropdown(
                        id="filter-segment",
                        className="dropdown",
                        options=[
                            {"label": i, "value": i}
                            for i in data.orders_per_segment_info["Segment"].unique()
                        ],
                        multi=True,
                        placeholder="Filter by Customer Segment...",
                        value=None,
                    ),
                    dcc.Dropdown(
                        id="filter-state",
                        className="dropdown",
                        options=[
                            {"label": i, "value": i}
                            for i in data.orders_per_state_info["State"].unique()
                        ],
                        multi=True,
                        placeholder="Filter by State...",
                        value=None,
                    ),
                    dcc.Dropdown(
                        id="filter-month",
                        className="dropdown",
                        options=[
                            {"label": i, "value": i}
                            for i in data.orders_per_month_info["Month"].unique()
                        ],
                        multi=True,
                        placeholder="Filter by Month...",
                        value=None,
                    ),
                    dcc.Dropdown(
                        id="filter-week",
                        className="dropdown",
                        options=[
                            {"label": i, "value": i}
                            for i in data.orders_per_week_info["Weekday"].unique()
                        ],
                        multi=True,
                        placeholder="Filter by Weekday...",
                        value=None,
                    ),
                ],
                className="filter-content",
            )
        ],
        className="component-section",
    )


# Principal Layout
def serve_layout():
    """
    Builds the main layout of the dashboard.
    :Returns: html.Div: Complete layout for the Dash app.
    """
    if data.df is None or data.df.empty:
        return html.Div(
            ["No data available to display the dashboard."],
            style={"padding": "2rem", "fontSize": "1.2rem"},
        )

    return html.Div(
        [
            header(),
            html.Hr(),
            # Filter bar
            html.Div(
                [
                    html.Div([filter_bar()], className="card-full", id="filter-bar"),
                ],
                className="row",
            ),
            # Shipping overview and modes
            html.Div(
                [
                    html.Div(className="card-half", id="avg_shipping"),
                    html.Div(className="card-half", id="shipping_modes"),
                ],
                className="row",
            ),
            # Segment and Location
            html.Div(
                [
                    html.Div(className="card-half", id="order_by_segment"),
                    html.Div(className="card-half", id="order_by_location"),
                ],
                className="row",
            ),
            # Trends
            html.Div(
                [
                    html.Div(className="card-full", id="order_trends"),
                ],
                className="row",
            ),
        ],
        id="app",
    )
