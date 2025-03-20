import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output
from datetime import datetime

app = dash.Dash(__name__)
app.title = "Dashboard Bitcoin"

def load_data():
    try:
        df = pd.read_csv("data/bitcoin_prices.csv", header=None, names=["Timestamp", "Price"])
        df["Price"] = df["Price"].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        return df
    except Exception as e:
        print("Erreur lors du chargement des données :", e)
        return pd.DataFrame(columns=["Timestamp", "Price"])

app.layout = html.Div([
    html.H1("Dashboard Bitcoin"),
    html.Div(id="latest-price", style={"fontSize": "24px", "marginBottom": "20px"}),
    dcc.Graph(id="price-graph"),
    html.Div(id="daily-report", style={"marginTop": "30px"}),
    dcc.Interval(id="interval-component", interval=5*60*1000, n_intervals=0)
])

@app.callback(
    [Output("latest-price", "children"),
     Output("price-graph", "figure"),
     Output("daily-report", "children")],
    [Input("interval-component", "n_intervals")]
)
def update_dashboard(n):
    df = load_data()
    if df.empty:
        return "Aucune donnée disponible", {}, "Aucun rapport à afficher"
    
    latest_value = df.iloc[-1]
    latest_text = f"Dernier prix relevé à {latest_value['Timestamp']:%Y-%m-%d %H:%M:%S} : {latest_value['Price']:.2f} USD"
    figure = {
        "data": [go.Scatter(x=df["Timestamp"], y=df["Price"], mode="lines+markers", name="Prix")],
        "layout": {"title": "Évolution du prix du Bitcoin", "xaxis": {"title": "Temps"}, "yaxis": {"title": "Prix (USD)"}}
    }
    current_hour = datetime.now().hour
    last_day = df["Timestamp"].dt.date.iloc[-1]
    daily_data = df[df["Timestamp"].dt.date == last_day]

    if current_hour >= 20 and not daily_data.empty:
        open_price = daily_data.iloc[0]["Price"]
        close_price = daily_data.iloc[-1]["Price"]
        volatility = daily_data["Price"].std()
        report = html.Div([
            html.H2("Rapport Quotidien"),
            html.P(f"Date : {last_day}"),
            html.P(f"Prix d'ouverture : {open_price:.2f} USD"),
            html.P(f"Prix de clôture : {close_price:.2f} USD"),
            html.P(f"Volatilité : {volatility:.2f}")
        ])
    else:
        report = "Le rapport quotidien sera disponible après 20h."
    
    return latest_text, figure, report

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
