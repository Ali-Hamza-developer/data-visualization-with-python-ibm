# Import required packages
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html

# Read the airline data into pandas dataframe
airline_data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
    encoding="ISO-8859-1",
    dtype={'Div1Airport': str, 'Div1TailNum': str, 
           'Div2Airport': str, 'Div2TailNum': str}
)

# Randomly sample 500 data points
data = airline_data.sample(n=500, random_state=42)

# Pie Chart Creation
fig = px.pie(
    data, 
    values='Flights', 
    names='DistanceGroup', 
    title='Distance group proportion by flights'
)

# Create a dash application
app = dash.Dash(__name__)

# Layout of the application
app.layout = html.Div(children=[
    html.H1("Airline Dashboard", style={'textAlign': 'center', 'color': '#003366'}),

    html.P("This dashboard displays the proportion of flights by distance group using a pie chart.", 
           style={'textAlign': 'center',  'color': '#F57241'}),

    dcc.Graph(
        id='pie-chart',
        figure=fig
    )
])

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
