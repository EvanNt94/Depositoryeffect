from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.graph_objects as go
import pandas as pd
import datetime  # Für Datumsmanipulation
from backend.AT.price.option import fetch_options_data_equity as get_option_data


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash()

app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Input("AAPL", id="TICKER"),
    dcc.Graph(id='graph-content')
]

@callback(
    Output('graph-content', 'figure'),
    Input('TICKER', 'value')
)
def update_graph(value):
    options_data = get_option_data(value)


    """
    Erstellt eine 3D-Volatilitätsoberflächengrafik mit Plotly, die der ersten Grafik ähnlicher sieht,
    basierend auf Optionsdaten.

    Args:
        options_data (dict): Ein Dictionary mit Optionsdaten im Format des Beispiels.

    Returns:
        plotly.graph_objects.Figure: Die erstellte Plotly-Figur.
    """

    # 1. Daten extrahieren und in Pandas DataFrame umwandeln (wie gehabt)
    data_rows = []
    option_values = options_data['values']
    for expiration_data in options_data['expirations']:
        expiration_date = expiration_data['date']
        for option in expiration_data['options']:
            strike_price = option['strike']
            iv = None
            if 'call' in option and 'id' in option['call']:
                call_option_id = option['call']['id']
                iv_key_call = f"{call_option_id}-iv"
                if iv_key_call in option_values:
                    iv = option_values[iv_key_call]
            elif 'put' in option and 'id' in option['put']:
                put_option_id = option['put']['id']
                iv_key_put = f"{put_option_id}-iv"
                if iv_key_put in option_values:
                    iv = option_values[iv_key_put]
            if iv is not None:
                data_rows.append({
                    'expiration': expiration_date,
                    'strike': strike_price,
                    'implied_volatility': iv
                })

    df = pd.DataFrame(data_rows)

    # 2. Daten für Plotly Surface vorbereiten (Pivot-Tabelle)
    pivot_df = df.pivot_table(index='expiration', columns='strike', values='implied_volatility')

    # Achsenwerte
    expiration_dates_str = pivot_df.index.to_list()
    strike_prices = pivot_df.columns.to_list()
    volatility_values = pivot_df.values

    # *** Verbesserungen für Ausrichtung und Darstellung ***

    # X-Achse: Strike Preise (wie in der ersten Grafik)
    x_axis_values = strike_prices
    x_axis_title = 'Strike Preis'

    # Y-Achse: Verfallsdaten (wie in der ersten Grafik, von "vorne" nach "hinten")
    y_axis_values = expiration_dates_str
    y_axis_title = 'Verfallsdatum'

    # Z-Achse: Implizite Volatilität (Höhe)
    z_axis_values = volatility_values
    z_axis_title = 'Implizite Volatilität'


    # 3. Plotly Surface Plot erstellen (angepasst)
    fig = go.Figure(data=[go.Surface(z=z_axis_values,
                                     x=x_axis_values,  # Strike Preise auf X-Achse
                                     y=y_axis_values,  # Verfallsdaten auf Y-Achse
                                     colorscale='Viridis')])

    # 4. Layout anpassen (verbessert für Ähnlichkeit zur ersten Grafik)
    fig.update_layout(
        title='Volatilitätsoberfläche',
        scene=dict(
            xaxis_title=x_axis_title,
            yaxis_title=y_axis_title,
            zaxis_title=z_axis_title,
            xaxis=dict(tickformat=".0f"), # Keine Dezimalstellen bei Strike-Preisen
            yaxis=dict(
                tickvals=y_axis_values, # Explizite Tick-Werte für Verfallsdaten
                ticktext=[datetime.datetime.strptime(d, '%Y-%m-%d').strftime('%b %d') for d in y_axis_values], # Formatierte Monats- und Tagesanzeige
                autorange='reversed' # Verfallsdaten von vorne nach hinten (früheste zuerst)
            ),
            camera=dict(                                 # Kameraperspektive anpassen
                eye=dict(x=1.2, y=-1.2, z=0.8)         # Position der Kamera (x, y, z Koordinaten)
            )
        ),
        margin=dict(l=20, r=20, b=20, t=40)
    )

    return fig

if __name__ == '__main__':
    app.server.run(port=8000, host='127.0.0.1')
