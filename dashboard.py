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

        # x_range_continent = max(continent_df["GDP per capita (US$)"]) + 1000
        # y_range_continent = max(continent_df["Oil Consumption per capita (tonnes per year)"]) + 5
        
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

        # Add annotations for wars
        wars_annotations = {
            'Asia': {
                'Vietnam': (1965, 1975),
                'Vietnam-China': (1979, 1991),
                'Indonesia-Malaysia': (1965, 1966),
                'India-Pakistan': (1965, 1969),
                'Korea': (1966, 1969),
                'Israel': (1967, 1970),
                'Cambodia': (1967, 1975),
                'Cambodia-Vietnam': (1978, 1989),
                'Soviet-Afghanistan': (1979, 1989),
                'Iran-Iraq': (1974, 1975),
                'Indonesia-Timor': (1975, 1976),
                'Iran-Iraq': (1980, 1988),
                'Malaysia': (1968, 1989),
                'Azerbaijan': (1988, 1994),
                'Gulf': (1990, 1991),
                'Iraq': (2003, 2004),
                'Afghanistan': (1989, 1992),
                'Iraq': (1994, 1997),
                'Afghanistan': (1996, 2002),
            },
            'Africa': {
                'Sudan': (1965, 1972),
                'Sudan': (1983, 2005),
                'Congo': (1960, 1966),
                'Egypt-Libya': (1977,),
                'Algeria': (1991, 2002),
                'Nigeria': (1967, 1970),
                'Somalia-Ethiopia': (1977, 1978),
                'Chad-Libya': (1978, 1987),
                'Uganda-Tanzania': (1978, 1979),
                'Yemen': (1979,),
                'Ethiopia-Somalia': (1982,),
                'Ethiopia': (1974, 1991),
                'Lebanon': (1975, 1990),
                'Angola': (1979, 2002),
                'Chad-Nigeria': (1983,),
                'Mauritania-Senegal': (1989, 1991),
                'Congo': (1996, 1997),
                'Congo': (1998, 2003),
                'Eritrea-Ethiopia': (1998, 2000),
                'Eritrea': (2008,),
            },
            'Europe': {
                'Chechen Rep.': (1994, 1996),
                'Chechen Rep.': (1999, 2000),
                'Georgia': (1991, 1993),
                'Albania': (1997,),
                'Kosovo': (1998, 1999),
            },
        }

        annotation_text = ''
        for continent_key, wars in wars_annotations.items():
            if continent == continent_key:
                for war, years_range in wars.items():
                    if len(years_range) == 1:
                        annotation_text += f'{war}<br>'
                    else:
                        start_year, end_year = years_range
                        if start_year <= year <= end_year:
                            annotation_text += f'{war}<br>'

        if annotation_text:
            fig.add_annotation(
                go.layout.Annotation(
                    xref="x",
                    yref="y",
                    x=x_range[1] - 0.4 * (x_range[1] - x_range[0]),
                    y=y_range[1] - 0.5 * (y_range[1] - y_range[0]),
                    text=f'<b>Wars ({year}):</b><br>{annotation_text}',
                    showarrow=False,
                    font=dict(size=10, color='black'),
                    align='left',
                    bordercolor='black',
                    borderwidth=1,
                ),
                row=1, col=i,
            )

    fig.update_layout(
        title=f'Mortality Rate vs Oil Consumption and GDP per capita in {year}',
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(size=12),
        coloraxis_showscale=False
    )

    return fig

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
