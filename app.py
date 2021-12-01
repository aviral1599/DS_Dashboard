import dash
import dash_core_components as dcc
#from dash import dcc
import dash_html_components as html
#from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

data = pd.read_csv("NIFTY50.csv")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__ , external_stylesheets=external_stylesheets)
server = app.server
app.title = "Stock Exchange Analytics"

app.layout = html.Div(
    children=[
        html.Div(
            children = [
                html.P(children="📉", className="header-emoji"),
                html.H1(
                    children="Stock Exchange Analytics",className="header-title",
                ),
                html.P(
                    children="Analyzing day wise high and low prices of indexes.",className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Share", className="menu-title"),
                        dcc.Dropdown(
                            id="share-filter",
                            options=[
                                {"label": share, "value": share}
                                for share in np.sort(data.Symbol.unique())
                            ],
                            value="ITC",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children = [
                html.Div(
                    children =
                        dcc.Graph(
                            id="open-price-chart", config={"displayModeBar": False},
                        ),
                        className="card",
                ),
                html.Div(
                    children =
                        dcc.Graph(
                            id="close-price-chart", config={"displayModeBar": False},
                        ),
                        className="card",
                ),      
                html.Div(
                    children =
                        dcc.Graph(
                            id="high-price-chart", config={"displayModeBar": False},
                        ),
                        className="card",
                ),
                html.Div(
                    children = 
                        dcc.Graph(
                            id="low-price-chart", config={"displayModeBar": False},
                        ),
                        className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

@app.callback(
    [Output("open-price-chart", "figure"), Output("close-price-chart", "figure") , Output("high-price-chart", "figure") , Output("low-price-chart", "figure")],
    [
        Input("share-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(share,start_date, end_date):
    mask = (
        (data.Symbol == share)
        & (data.Date >= start_date)
        & (data.Date <= end_date)
    )
    filtered_data = data.loc[mask, :]
    open_price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Open"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Opening Price of Share.",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    close_price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Close"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {
                "text": "Closing Price of Share.",
                "x": 0.05,
                "xanchor": "left"
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    
    high_price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["High"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Highest Price of Share.",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#3333ff"],
        },
    }
    
    low_price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Low"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Lowest Price of Share.",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#ffff00"],
        },
    }
    return open_price_chart_figure, close_price_chart_figure , high_price_chart_figure , low_price_chart_figure

if __name__ == "__main__":
    app.run_server(debug=True)