import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Dropdown list to select Launch Site
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'ALL SITES', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True),
    
    html.Br(),

    # TASK 2: Pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Slider to select payload range
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    value=[min_payload, max_payload],
                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'}),
    
    # TASK 4: Scatter chart to show correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback to render the pie chart based on selected site
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def build_pie_chart(site_dropdown):
    if site_dropdown == 'ALL':
        # Show the total success count for all sites
        piechart = px.pie(spacex_df, 
                          names='Launch Site', 
                          values='class', 
                          title='Total Successful Launches for All Sites')
        return piechart
    else:
        # Filter the dataframe based on the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == site_dropdown]
        
        # Map class values (0 and 1) to "Failure" and "Success"
        filtered_df['class'] = filtered_df['class'].map({1: 'Success', 0: 'Failure'})
        
        # Generate pie chart for the specific site showing Success vs Failure
        piechart = px.pie(filtered_df, 
                          names='class', 
                          title=f'Total Success and Failure Launches for {site_dropdown}')
        return piechart

# TASK 4: Callback to render the scatter plot based on selected site and payload range
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')])
def update_scatter_plot(site_dropdown, payload_slider):
    low, high = payload_slider
    if site_dropdown == 'ALL':
        # Filter data based on the payload range
        filtered_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) &
                                  (spacex_df['Payload Mass (kg)'] <= high)]
        scatterplot = px.scatter(filtered_data, 
                                 x="Payload Mass (kg)", 
                                 y="class", 
                                 color="Booster Version Category",
                                 title="Correlation between Payload and Success for All Sites")
        return scatterplot
    else:
        # Filter by both site and payload range
        filtered_df = spacex_df[(spacex_df['Launch Site'] == site_dropdown) &
                                (spacex_df['Payload Mass (kg)'] >= low) &
                                (spacex_df['Payload Mass (kg)'] <= high)]
        scatterplot = px.scatter(filtered_df, 
                                 x="Payload Mass (kg)", 
                                 y="class", 
                                 color="Booster Version Category",
                                 title=f"Correlation between Payload and Success for {site_dropdown}")
        return scatterplot

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
