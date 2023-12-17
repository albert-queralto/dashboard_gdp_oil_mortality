from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

df = pd.read_csv("oil_consumption_mortality.csv")
app = Dash(__name__)
server = app.server

years = list(set([year for year in df["Year"] if year % 1 == 0]))
years.sort()

continents = list(set(df["Continent"]))

oil_prod_10M_12M_barrels_day = ['United States', 'Saudi Arabia', 'Russia']
oil_prod_1M_5M_barrels_day = [    
    'Canada', 'China', 'Brazil', 'Iraq', 'Iran', 'Libya',
    'United Arab Emirates', 'Kuwait', 'Kazakhstan', 'Angola',
    'Mexico', 'Norway', 'Qatar', 'Oman', 'Nigeria', 'Algeria'
]
oil_prod_500k_1M_barrels_day = [
    'Colombia', 'United Kingdom', 'Venezuela', 'Azerbaijan',
    'Indonesia', 'India', 'Argentina', 'Egypt', 'Malaysia'
]
oil_prod_100k_500k_barrels_day = [
    'Ecuador', 'Australia', 'Guyana', 'Congo, Rep.', 'Gabon',
    'Turkmenistan', 'Bahrein', 'Ghana', 'Vietnam', 'South Sudan',
    'Thailand', 'Equatorial Guinea',
]
oil_prod_10k_100k_barrels_day = [
    'Syria', 'Italy', 'Brunei', 'Chad', 'Pakistan', 'Turkey',
    'Sudan', 'Denmark', 'Romania', 'Cameroon', 'Trinidad and Tobago',
    'Yemen', 'Peru', 'Papua New Guinea', 'Uzbekistan',
    'Tunisia', 'Germany', 'Cuba', 'Belarus', 'Cote d\'Ivoire',
    'Netherlands', 'Bolivia', 'Congo, Dem. Rep.', 'Hungary',
    'Poland', 'Mongolia', 'Albania', 'Serbia', 'East Timor',
    'Suriname', 'France', 'Croatia'
]

df['Oil Producing Countries'] = df['Country'].apply(
    lambda x: '10M-12M barrels/day' 
    if x in oil_prod_10M_12M_barrels_day else (
    '1M-5M barrels/day'
    if x in oil_prod_1M_5M_barrels_day else (
    '500k-1M barrels/day'
    if x in oil_prod_500k_1M_barrels_day else (
    '100k-500k barrels/day'
    if x in oil_prod_100k_500k_barrels_day else (
    '10k-100k barrels/day'
    if x in oil_prod_10k_100k_barrels_day else (
    '<10k barrels/day'
    ))))))

def create_density_contour_fig(year, continents):
    mask = (df["Continent"].isin(continents) & (df["Year"] == year))
    filtered_df = df.loc[mask]
    mortality_levels = [50, 100, 200, 400]
    levels_text = ['Low (50)', 'Medium (100)', 'High (200)', 'Very High (400)']
    
    colors = ['#648fff', '#785ef0', '#dc267f', '#fe6100', '#ffb000']
    
    x_range = [
        0,
        max(filtered_df["GDP per capita (US$)"]) + 1000
    ]
    
    y_range = [
        0,
        max(filtered_df["Oil Consumption per capita (tonnes per year)"]) + 5
    ]
    
    fig = make_subplots(
        rows=1,
        cols=len(continents),
        subplot_titles=continents,
        shared_xaxes=False,
        shared_yaxes=False,
        horizontal_spacing=0.05,
    )

    for i, continent in enumerate(continents, start=1):
        continent_df = filtered_df[filtered_df["Continent"] == continent]
        hist2d_contour = go.Histogram2dContour(
            x=continent_df["GDP per capita (US$)"],
            y=continent_df["Oil Consumption per capita (tonnes per year)"],
            z=continent_df["Mortality Rate"],
            histfunc="avg",
            colorscale=colors,
            autocontour=False,
            contours_coloring="fill",
            line=dict(width=1),
            hovertemplate="Mortality Rate: %{z}<br>Oil Consumption: %{y}<br>GDP per capita: %{x}<extra></extra>",
            showscale=True,
            contours=dict(
                start=min(mortality_levels),
                end=max(mortality_levels),
                size=(max(mortality_levels) - min(mortality_levels)) / len(mortality_levels),
            ),
            colorbar=dict(
                title="Mortality Rate (per 1000 births)",
                tickvals=mortality_levels,
                ticktext=levels_text,
            ),
        )

        fig.add_trace(hist2d_contour, row=1, col=i)
        fig.update_xaxes(title_text="GDP per capita (US$)", title_standoff=5,
                        range=x_range,
                        title_font_size=14, row=1, col=i)
        fig.update_yaxes(title_text="Oil Consumption per<br>capita (tonnes per year)",
                        title_standoff=0, title_font_size=14,
                        range=y_range,
                        row=1, col=i)

    fig.update_layout(
        title=f'Mortality Rate vs Oil Consumption and GDP per capita in {year}',
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(size=12),
        coloraxis_showscale=False
    )

    return fig

# def create_scatter_fig(year, continents):
#     mask = (df["Continent"].isin(continents) & (df["Year"] == year))
#     return px.scatter(
#         df.loc[mask],
#         x="Mortality Rate",
#         y="Oil Consumption per capita (tonnes per year)",
#         size="GDP per capita (US$)",
#         color="Continent",
#         hover_name="Country",
#         labels={
#                     "Oil Consumption per capita (tonnes per year)": "Oil Consumption per capita<br>(tonnes per year)",
#                     "Country": "Country",
#                     "Continent": "Continent",
#                     "Mortality Rate": "Mortality Rate (per 1000 births)",
#                 },
#         log_x=False,
#         size_max=55,
#         title=f'Mortality Rate vs Oil Consumption per capita in {year}',
#     ).update_layout(
#         xaxis=dict(range=[-df["Mortality Rate"].max() * 0.2, df["Mortality Rate"].max() * 1.1]),
#         yaxis=dict(range=[-df["Oil Consumption per capita (tonnes per year)"].max() * 0.2, df["Oil Consumption per capita (tonnes per year)"].max() * 1.1]),
#         margin=dict(l=20, r=20, t=30, b=20),
#         font=dict(size=12)
#     )

def create_mortality_bar_fig(year, continents):
    mask = (df["Continent"].isin(continents) & (df["Year"] == year))
    top_10 = df[mask].nlargest(10, 'Mortality Rate')
    top_10 = top_10.sort_values(by='Mortality Rate', ascending=True)
    top_10.reset_index(drop=True, inplace=True)
    
    mortality_levels = [50, 100, 200, 400]
    levels_text = ['Low (50)', 'Medium (100)', 'High (200)', 'Very High (400)']
    alpha_mapping = {
        50: 0.15,
        100: 0.3,
        200: 0.55,
        400: 0.8
    }
    color_mapping = {
        'Asia': '#648fff',
        'Europe': '#785ef0',
        'Africa': '#dc267f',
        'North America':'#fe6100',
        'South America': '#ffb000',
        'Oceania': '#054fb9'
    }
    
    def get_alpha(rate):
        if rate <= 50:
            return alpha_mapping[50]
        elif rate <= 100:
            return alpha_mapping[100]
        elif rate <= 200:
            return alpha_mapping[200]
        elif rate <= 400:
            return alpha_mapping[400]
        else:
            return 1
    
    def get_color(continent):
        return color_mapping[continent]

    top_10['alpha'] = top_10['Mortality Rate'].apply(get_alpha)
    top_10['color'] = top_10['Continent'].apply(get_color)
    
    shapes = []
    annotations = []

    for level, text in zip(mortality_levels, levels_text):
        shapes.append(
            dict(
                type='line',
                x0=level,
                x1=level,
                y0=-1,
                y1=len(top_10),
                line=dict(color='black', width=1)
            )
        )

        annotations.append(
            dict(
                x=level-20,
                y=len(top_10) // 2 + 0.5,
                text=text,
                showarrow=False,
                font=dict(size=12),
                textangle=90
            )
        )

    traces = []
    legend_labels = set()

    for i, row in top_10.iterrows():
        alpha = row['alpha']
        continent = row['Continent']

        if continent not in legend_labels:
            legend_labels.add(continent)
            traces.append(go.Bar(
                x=[None],
                y=[None],
                legendgroup=continent,
                name=continent,
                marker=dict(color=color_mapping[continent]),
                showlegend=True
            ))

        traces.append(go.Bar(
            x=[row['Mortality Rate']],
            y=[i],
            orientation='h',
            marker=dict(
                color=row['color'],
                opacity=alpha
            ),
            legendgroup=continent,
            showlegend=False,
            name=continent,
            hovertemplate=f"Continent: {continent}<br>Mortality Rate: {row['Mortality Rate']}<br>Country: {row['Country']}"
        ))

    layout = go.Layout(
        title=f'Top 10 Countries by Mortality Rate in {year}',
        xaxis=dict(title='Mortality Rate (per 1000 births)', 
                range=[0, df["Mortality Rate"].max() * 1.1], title_standoff=0),
        yaxis=dict(title='Country', categoryorder='total ascending',
                tickvals=top_10.index, ticktext=top_10['Country'], title_standoff=0),
        margin=dict(l=20, r=20, t=30, b=20),
        font=dict(size=12),
        xaxis_autorange=False,
        yaxis_autorange=True,
        legend=dict(title='Continent', traceorder='reversed', itemclick='toggleothers', itemdoubleclick='toggle'),
        shapes=shapes,
        annotations=annotations
    )

    fig = go.Figure(data=traces, layout=layout)

    return fig

def create_oil_bar_fig(year, continents):
    mask = (df["Continent"].isin(continents) & (df["Year"] == year))
    top_10 = df[mask].nlargest(10, 'Oil Consumption per capita (tonnes per year)')
    top_10 = top_10.sort_values(by='Oil Consumption per capita (tonnes per year)', ascending=True)
    top_10.reset_index(drop=True, inplace=True)
    
    oil_levels = [2, 4, 7.5, 10]
    levels_text = ['Low (2)', 'Medium (4)', 'High (7.5)', 'Very High (10)']
    alpha_mapping = {
        2: 0.15,
        4: 0.3,
        7.5: 0.55,
        10: 0.8
    }
    color_mapping = {
        'Asia': '#648fff',
        'Europe': '#785ef0',
        'Africa': '#dc267f',
        'North America':'#fe6100',
        'South America': '#ffb000',
        'Oceania': '#054fb9'
    }
    
    def get_alpha(rate):
        if rate <= 2:
            return alpha_mapping[2]
        elif rate <= 4:
            return alpha_mapping[4]
        elif rate <= 7.5:
            return alpha_mapping[7.5]
        elif rate <= 10:
            return alpha_mapping[10]
        else:
            return 1

    def get_color(continent):
        return color_mapping[continent]

    top_10['alpha'] = top_10['Oil Consumption per capita (tonnes per year)'].apply(get_alpha)
    top_10['color'] = top_10['Continent'].apply(get_color)
    
    shapes = []
    annotations = []

    for level, text in zip(oil_levels, levels_text):
        shapes.append(
            dict(
                type='line',
                x0=level,
                x1=level,
                y0=-1,
                y1=len(top_10),
                line=dict(color='black', width=1)
            )
        )

        annotations.append(
            dict(
                x=level-0.5,
                y=len(top_10) // 2 + 0.5,
                text=text,
                showarrow=False,
                font=dict(size=12),
                textangle=90
            )
        )
        
    traces = []
    legend_labels = set()

    for i, row in top_10.iterrows():
        alpha = row['alpha']
        continent = row['Continent']

        if continent not in legend_labels:
            legend_labels.add(continent)
            traces.append(go.Bar(
                x=[None],
                y=[None],
                legendgroup=continent,
                name=continent,
                marker=dict(color=color_mapping[continent]),
                showlegend=True
            ))

        traces.append(go.Bar(
            x=[row['Oil Consumption per capita (tonnes per year)']],
            y=[i],
            orientation='h',
            marker=dict(
                color=row['color'],
                opacity=alpha
            ),
            legendgroup=continent,
            showlegend=False,
            name=continent,
            hovertemplate=f"Continent: {continent}<br>Oil Consumption per capita: {row['Oil Consumption per capita (tonnes per year)']}<br>Country: {row['Country']}<br>Oil Production: {row['Oil Producing Countries']}"
        ))

    layout = go.Layout(
        title=dict(
            text=f'Top 10 Countries by Oil Consumption<br>per capita (tonnes per year) in {year}',
            y=0.95
        ),
        xaxis=dict(title='Oil Consumption per<br>capita (tonnes per year)', 
                range=[0, df["Oil Consumption per capita (tonnes per year)"].max() * 1.1],
                title_standoff=0),
        yaxis=dict(title='Country', categoryorder='total ascending', tickvals=top_10.index, 
                ticktext=top_10['Country'], title_standoff=0),
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(size=12),
        xaxis_autorange=False,
        yaxis_autorange=True,
        legend=dict(title='Continent', traceorder='reversed', itemclick='toggleothers', itemdoubleclick='toggle'),
        shapes=shapes,
        annotations=annotations
    )

    fig = go.Figure(data=traces, layout=layout)

    return fig

def create_gdp_bar_fig(year, continents):
    mask = (df["Continent"].isin(continents) & (df["Year"] == year))
    top_10 = df[mask].nlargest(10, 'GDP per capita (US$)')
    top_10 = top_10.sort_values(by='GDP per capita (US$)', ascending=True)
    top_10.reset_index(drop=True, inplace=True)
    
    gdp_levels = [5000, 20000, 40000, 70000]
    levels_text = ['Low (5000)', 'Medium (20000)', 'High (40000)', 'Very High (70000)']
    alpha_mapping = {
        5000: 0.15,
        20000: 0.3,
        40000: 0.55,
        70000: 0.8
    }
    color_mapping = {
        'Asia': '#648fff',
        'Europe': '#785ef0',
        'Africa': '#dc267f',
        'North America':'#fe6100',
        'South America': '#ffb000',
        'Oceania': '#054fb9'
    }
    
    def get_alpha(rate):
        if rate <= 5000:
            return alpha_mapping[5000]
        elif rate <= 20000:
            return alpha_mapping[20000]
        elif rate <= 40000:
            return alpha_mapping[40000]
        elif rate <= 70000:
            return alpha_mapping[70000]
        else:
            return 1
    
    def get_color(continent):
        return color_mapping[continent]

    top_10['alpha'] = top_10['GDP per capita (US$)'].apply(get_alpha)
    top_10['color'] = top_10['Continent'].apply(get_color)
    
    shapes = []
    annotations = []

    for level, text in zip(gdp_levels, levels_text):
        shapes.append(
            dict(
                type='line',
                x0=level,
                x1=level,
                y0=-1,
                y1=len(top_10),
                line=dict(color='black', width=1)
            )
        )

        annotations.append(
            dict(
                x=level-1500,
                y=len(top_10) // 2 + 0.5,
                text=text,
                showarrow=False,
                font=dict(size=12),
                textangle=90
            )
        )

    traces = []
    legend_labels = set()

    for i, row in top_10.iterrows():
        alpha = row['alpha']
        continent = row['Continent']

        if continent not in legend_labels:
            legend_labels.add(continent)
            traces.append(go.Bar(
                x=[None],
                y=[None],
                legendgroup=continent,
                name=continent,
                marker=dict(color=color_mapping[continent]),
                showlegend=True
            ))

        traces.append(go.Bar(
            x=[row['GDP per capita (US$)']],
            y=[i],
            orientation='h',
            marker=dict(
                color=row['color'],
                opacity=alpha
            ),
            legendgroup=continent,
            showlegend=False,
            name=continent,
            hovertemplate=f"Continent: {continent}<br>GDP per capita (US$): {row['GDP per capita (US$)']}<br>Country: {row['Country']}"
        ))

    layout = go.Layout(
        title=dict(
            text=f'Top 10 Countries by GDP per capita (US$) in {year}',
            y=0.95
        ),
        xaxis=dict(title='GDP per capita (US$)', 
                range=[0, df["GDP per capita (US$)"].max() * 1.1],
                title_standoff=0),
        yaxis=dict(title='Country', categoryorder='total ascending', tickvals=top_10.index, 
                ticktext=top_10['Country'], title_standoff=0),
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(size=12),
        xaxis_autorange=False,
        yaxis_autorange=True,
        legend=dict(title='Continent', traceorder='reversed', itemclick='toggleothers', itemdoubleclick='toggle'),
        shapes=shapes,
        annotations=annotations
    )

    fig = go.Figure(data=traces, layout=layout)

    return fig

app.layout = html.Div(
    [
        html.H2(children='Mortality rate based on oil consumption and GDP per capita'),
        html.Div(style={'margin': '0px 0px -10px 0px'}),
        
        html.Div(
            children=[
                html.Div(dcc.Checklist(
                    id="checklist",
                    options=[
                        {"label": continent, "value": continent} for continent in df["Continent"].unique()
                    ],
                    value=df["Continent"].unique().tolist(),
                    inline=True,
                    style={'display': 'inline-block'}
                ), style={'display': 'inline-block', 'margin': '0px 20px 0px 0px'}),
                
                html.Div(dcc.Slider(
                    id="year-slider",
                    min=df["Year"].min(),
                    max=df["Year"].max(),
                    value=df["Year"].min(),
                    marks={str(year-1): str(year-1) for year in years if year % 2 == 0},
                    step=None,
                ), style={'width': '60%', 'display': 'inline-block', 'margin': '0px 20px 0px 0px'}),
                
                html.Button("Play", id="play", style={'width': '5%', 'display': 'inline-block'}),
            ],
            style={'margin': '0px 0px'}
        ),
        
        dcc.Interval(id="animate", interval=3000, disabled=True),
        
        dcc.Graph(id="graph-with-slider3", style={'height': '250px', 'margin': '10px 0px'}, figure=create_density_contour_fig(df["Year"].min(), df["Continent"].unique().tolist())),
        
        html.Div(
            children=[
                dcc.Graph(
                    id="graph-with-slider", 
                    style={'width': '48%', 'height': '275px', 'display': 'inline-block', 'margin': '0px', 'padding': '0px'}, 
                    figure=create_mortality_bar_fig(df["Year"].min(), df["Continent"].unique().tolist())
                ),
                dcc.Graph(
                    id="graph-with-slider2",
                    style={'width': '48%', 'height': '275px', 'display': 'inline-block', 'margin': '0px', 'padding': '0px'}, 
                    figure=create_oil_bar_fig(df["Year"].min(), df["Continent"].unique().tolist())
                ),
                # dcc.Graph(
                #     id="graph-with-slider4",
                #     style={'width': '33%', 'height': '275px', 'display': 'inline-block', 'margin': '0px', 'padding': '0px'}, 
                #     figure=create_gdp_bar_fig(df["Year"].min(), df["Continent"].unique().tolist())
                # ),
            ],
            style={'margin': '10px 0px'}
        ),
        html.Div([
            html.P('The proprietary of the data used in this dashboard is The World Bank (CC BY-4.0 license).'),
        ])
    ]
)


@app.callback(
    Output("graph-with-slider", "figure"),
    Output("graph-with-slider2", "figure"),
    # Output("graph-with-slider4", "figure"),
    Output("graph-with-slider3", "figure"),
    Output("year-slider", "value"),
    Input("animate", "n_intervals"),
    State("year-slider", "value"),
    State("checklist", "value"),
    prevent_initial_call=True,
)

def update_figures(n, selected_year, continents):
    index = years.index(selected_year)
    index = (index + 1) % len(years)
    year = years[index]

    return (
        create_mortality_bar_fig(year, continents), 
        create_oil_bar_fig(year, continents),
        # create_gdp_bar_fig(year, continents),
        create_density_contour_fig(year, continents),
        year
    )


@app.callback(
    Output("animate", "disabled"),
    Input("play", "n_clicks"),
    State("animate", "disabled"),
)
def toggle(n, playing):
    if n:
        return not playing
    return playing

if __name__ == '__main__':
    app.run_server(debug=False)
