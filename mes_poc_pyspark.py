import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load dataset
df = pd.read_excel("Bakery.xlsx")

# Clean data
df = df.dropna()
df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce")
df["Cost"] = pd.to_numeric(df["Cost"], errors="coerce")
df["Profit"] = df["Revenue"] - df["Cost"]

# Create Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("European Bakery Sales Dashboard", style={'textAlign': 'center'}),

    # Filters
    html.Div([
        dcc.Dropdown(
            id='city_filter',
            options=[{'label': c, 'value': c} for c in df['City'].unique()],
            multi=True,
            placeholder="Select City"
        ),

        dcc.Dropdown(
            id='product_filter',
            options=[{'label': p, 'value': p} for p in df['Product'].unique()],
            multi=True,
            placeholder="Select Product"
        ),
    ]),

    # Charts
    dcc.Graph(id='revenue_chart'),
    dcc.Graph(id='profit_chart'),
    dcc.Graph(id='scatter_chart')
])

# Callbacks
@app.callback(
    [Output('revenue_chart', 'figure'),
     Output('profit_chart', 'figure'),
     Output('scatter_chart', 'figure')],
    [Input('city_filter', 'value'),
     Input('product_filter', 'value')]
)
def update_dashboard(city, product):

    filtered_df = df.copy()

    if city:
        filtered_df = filtered_df[filtered_df['City'].isin(city)]

    if product:
        filtered_df = filtered_df[filtered_df['Product'].isin(product)]

    # Revenue by city
    fig1 = px.bar(filtered_df, x="City", y="Revenue", color="City",
                  title="Revenue by City")

    # Profit by product
    fig2 = px.bar(filtered_df, x="Product", y="Profit", color="Product",
                  title="Profit by Product")

    # Scatter plot
    fig3 = px.scatter(filtered_df, x="Cost", y="Revenue",
                      size="Profit", color="City",
                      title="Cost vs Revenue")

    return fig1, fig2, fig3


# Run server
if __name__ == '__main__':
    app.run(debug=True)