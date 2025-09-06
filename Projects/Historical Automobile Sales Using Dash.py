# ===== Imports =====
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# ===== Data: load the assignment CSV from IBM Cloud =====
data = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/"
    "historical_automobile_sales.csv"
)

# ===== Dash app init =====
app = dash.Dash(__name__)

# Years for dropdown (derived from data)
year_list = sorted(data['Year'].unique())

# ===== Layout (Title, Dropdowns, Output container) =====
app.layout = html.Div(children=[
    # App title (Task 2.1)
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}
    ),

    # Report-type dropdown (Task 2.2)
    html.Label("Select Report Type:", style={'font-size': 20, 'padding': '10px'}),
    dcc.Dropdown(
        id='dropdown-statistics',
        options=[
            {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
            {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
        ],
        placeholder='Select a report type',
        value='Select Statistics',
        style={'width': '80%', 'padding': '3px', 'font-size': 20, 'text-align-last': 'center'}
    ),

    html.Br(),

    # Year dropdown (Task 2.2)
    html.Label("Select Year:", style={'font-size': 20, 'padding': '10px'}),
    dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        placeholder='Select year',
        value='Select-year',
        style={'width': '80%', 'padding': '3px', 'font-size': 20, 'text-align-last': 'center'}
    ),

    html.Br(),

    # Output container where graphs will be rendered (Task 2.3)
    html.Div([
        html.Div(id='output-container', className='chart-grid',
                 style={'display': 'flex', 'flex-wrap': 'wrap'})
    ])
])

# ===== Callback: update output charts based on selections (Task 2.4) =====
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output_container(selected_statistics, selected_year):
    """
    Renders four charts depending on the report type.
    - Recession Period Statistics: filter Recession == 1 and show 4 charts.
    - Yearly Statistics: filter selected Year and show 4 charts.
    """

    # --- Recession report: filter Recession == 1 and plot 4 visuals ---
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        return [
            # 1) Sales by vehicle type (sum)
            html.Div(dcc.Graph(figure=px.bar(
                recession_data.groupby('Vehicle_Type')['Automobile_Sales'].sum().reset_index(),
                x='Vehicle_Type', y='Automobile_Sales',
                title="Sales by Vehicle Type during Recession"
            )), style={'width': '48%'}),

            # 2) Total sales over recession years (sum by Year)
            html.Div(dcc.Graph(figure=px.line(
                recession_data.groupby('Year')['Automobile_Sales'].sum().reset_index(),
                x='Year', y='Automobile_Sales',
                title="Total Sales Over Recession Years"
            )), style={'width': '48%'}),

            # 3) GDP trend during recession (mean by Year)
            html.Div(dcc.Graph(figure=px.line(
                recession_data.groupby('Year')['GDP'].mean().reset_index(),
                x='Year', y='GDP',
                title="GDP during Recession"
            )), style={'width': '48%'}),

            # 4) Advertising expenditure trend during recession (mean by Year)
            html.Div(dcc.Graph(figure=px.line(
                recession_data.groupby('Year')['Advertising_Expenditure'].mean().reset_index(),
                x='Year', y='Advertising_Expenditure',
                title="Advertising Expenditure during Recession"
            )), style={'width': '48%'})
        ]

    # --- Yearly report: filter by selected Year and plot 4 visuals ---
    elif selected_statistics == 'Yearly Statistics' and selected_year != 'Select-year':
        year = int(selected_year)
        yearly_data = data[data['Year'] == year]

        return [
            # 1) Sales by vehicle type in the selected year (sum)
            html.Div(dcc.Graph(figure=px.bar(
                yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].sum().reset_index(),
                x='Vehicle_Type', y='Automobile_Sales',
                title=f"Sales by Vehicle Type in {year}"
            )), style={'width': '48%'}),

            # 2) Sales share by vehicle type (pie)
            html.Div(dcc.Graph(figure=px.pie(
                yearly_data, names='Vehicle_Type', values='Automobile_Sales',
                title=f"Sales Share by Vehicle Type in {year}"
            )), style={'width': '48%'}),

            # 3) Monthly sales trend (sum by Month)
            html.Div(dcc.Graph(figure=px.line(
                yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index(),
                x='Month', y='Automobile_Sales',
                title=f"Monthly Sales Trend in {year}"
            )), style={'width': '48%'}),

            # 4) Monthly advertising expenditure trend (mean by Month)
            html.Div(dcc.Graph(figure=px.line(
                yearly_data.groupby('Month')['Advertising_Expenditure'].mean().reset_index(),
                x='Month', y='Advertising_Expenditure',
                title=f"Advertising Trend in {year}"
            )), style={'width': '48%'})
        ]

    # Default: nothing selected → return empty container
    else:
        return []

# ===== Run server =====
if __name__ == '__main__':
    app.run(debug=True)
