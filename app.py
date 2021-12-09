#importing libraries
import dash #This library is used to initialize the dash application.
import dash_core_components as dcc #This library is used to add graphs,other visual components.
import dash_html_components as html # This library is used to include html tags.
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input #This library is used Input and Output .

data = pd.read_csv("NIFTY50.csv")#Reading the csv file.
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")#Manipulating the date.
data.sort_values("Date", inplace=True)#sorting data according to date

#linking external stylesheet
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

#Initialising application.
app = dash.Dash(__name__ , external_stylesheets=external_stylesheets)
server = app.server#eploy on Server
app.title = "Stock Exchange Analytics"

#Defining the Layout of Your Dash Application
app.layout = html.Div(
    children=[
        #Code for Header of the app
        html.Div(
            children = [
                html.P(children="📉", className="header-emoji"), #className argument to apply custom styles to your Dash components.c
                html.H1(
                    children="NIFTY-50 Stocks Analytics",className="header-title",
                ),
                html.P(
                    children="NIFTY-50 Stock Market Data (2000 - 2021) . Stock price data of the fifty stocks in NIFTY-50 index from NSE India",className="header-description",
                ),
            ],
            className="header",
        ),
        #code for Selecting and Filtering Data(Adding Interactive Components,menu that the user will use to interact with the data)
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Share", className="menu-title"),
                        dcc.Dropdown(            #dropdown to filter the data according to name of share
                            id="share-filter",     #identifier of this element
                            options=[                #options shown when the dropdown is selected
                                {"label": share, "value": share}
                                for share in np.sort(data.Symbol.unique())
                            ],
                            value="ITC", #Default value
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
                        dcc.DatePickerRange(    #date range selector to filter the data according to timeframe selected
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
        #Code for Dcc.Graph Components (Building Charts)
        html.Div(
            children = [
                #Code for Graph of Opening Prices of particulat Share everyday given timeframe
                html.Div(
                    children =
                        dcc.Graph(
                            id="open-price-chart", config={"displayModeBar": False},#specifying graph id and configuartion options 
                        ),
                        className="card",
                ),
                #Code for Graph of Closing Prices of particulat Share everyday in given timeframe
                html.Div(
                    children =
                        dcc.Graph(
                            id="close-price-chart", config={"displayModeBar": False},
                        ),
                        className="card",
                ),     
                #Code for Graph of Highest Prices of particulat Share everyday in given timeframe 
                html.Div(
                    children =
                        dcc.Graph(
                            id="high-price-chart", config={"displayModeBar": False},
                        ),
                        className="card",
                ),
                #Code for Graph of Lowest Prices of particulat Share everyday in given timeframe 
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

#callback function used for updating the graphs
@app.callback(
    [Output("open-price-chart", "figure"), Output("close-price-chart", "figure") , Output("high-price-chart", "figure") , Output("low-price-chart", "figure")], #The identifier of the element that they’ll modify when the function executes,The property of the element to be modified
    [   
        #property of the watched element that they should take when a change happens
        Input("share-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(share,start_date, end_date):
    mask = (
        (data.Symbol == share)
        & (data.Date >= start_date) #date should be between specified start and end date
        & (data.Date <= end_date)
    )
    filtered_data = data.loc[mask, :]
    #figure argument for dcc.graphs generated by a callback function using the inputs the user sets 
    open_price_chart_figure = {
        #specifying data attributes for the graph 
        "data": [
            {
                "x": filtered_data["Date"],#x data
                "y": filtered_data["Open"],#y data
                "type": "lines",# type of graph
                "hovertemplate": "Rs%{y:.2f}<extra></extra>",#hovertext
            },
        ],
        #specifying layout attributes of the graph
        "layout": {
            "title": {
                "text": "Opening Price of Share.",
                "x": 0.05, #sets the x position with respect to xref in normalized coordinates from 0(left) to 1(right)
                "xanchor": "left", #sets title horizontal alignment with respect to its x position 
            },
            "xaxis": {"fixedrange": True},#xaxis range
            "yaxis": {"tickprefix": "Rs", "fixedrange": True},#yaxis range
            "colorway": ["#17B897"],#sets the graoh color
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
                "hovertemplate": "Rs%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Highest Price of Share.",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "Rs", "fixedrange": True},
            "colorway": ["#3333ff"],
        },
    }
    
    low_price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Low"],
                "type": "lines",
                "hovertemplate": "Rs%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Lowest Price of Share.",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "Rs", "fixedrange": True},
            "colorway": ["#ffff00"],
        },
    }
    return open_price_chart_figure, close_price_chart_figure , high_price_chart_figure , low_price_chart_figure

#run your application
if __name__ == "__main__":
    app.run_server(debug=True)