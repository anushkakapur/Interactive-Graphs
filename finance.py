import yfinance as yf
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go

app = dash.Dash(__name__, suppress_callback_exceptions = True)
app.layout = html.Div(
    [
        dcc.Input(id="dfalse", type="text", placeholder="Debounce False"),
        html.Br(),
        html.Div(id="text"),
        dcc.Graph(id='graph-output', figure = {})
    ]
)


@app.callback(
    Output("graph-output", "figure"),
    Input("dfalse", "value")
)
def number_render(ticker):
    ticker = str(ticker)
    stock=yf.Ticker(ticker)
    reco = stock.recommendations.reset_index()
    recommend=reco.tail(10)[['To Grade', 'Date']]
    plot= recommend.groupby(['To Grade'])['Date'].count().reset_index()
    plot.rename(columns={'Date':'Count'}, inplace=True)
    fig = px.bar(plot, x='To Grade', y='Count')
    fig.update_layout(title = f'Analyst recommendation over the past 10 ratings for {ticker}')

    return fig


    app.layout = html.Div(children=[
        html.H1(children='Financial Analysis Dashboard'),

        html.Div(children='''
            Please enter a ticker with quotes (eg.'MSFT') to see plots
        '''),

        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ])

if __name__ == '__main__':
    app.run_server(debug=True)

