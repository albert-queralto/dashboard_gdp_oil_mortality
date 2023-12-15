from dash import Dash, dcc, html, Input, Output, State
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

df = pd.read_csv("oil_consumption_mortality.csv")
app = Dash(__name__)
server = app.server

years = list(set([year for year in df["Year"] if year % 1 == 0]))
years.sort()

continents = list(set(df["Continent"]))

# def create_density_contour_fig(year, continents):
#     mask = (df["Continent"].isin(continents) & (df["Year"] == year))
#     filtered_df = df.loc[mask]
#     filtered_df.loc[:, 'log_GDP'] = np.log(filtered_df['GDP per capita (US$)'])
#     return px.density_contour(
#         filtered_df,
#         x="Mortality Rate",
#         y="Oil Consumption per capita (tonnes per year)",
#         z="GDP per capita (US$)",
#         histfunc="sum",
#         histnorm="percent",
#         facet_col="Continent",
#         labels={
#                     "Oil Consumption per capita (tonnes per year)": "Oil Consumption per capita<br>(tonnes per year)",
#                     "Country": "Country",
#                     "Continent": "Continent",
#                     "Mortality Rate": "Mortality Rate (per 1000 births)",
#                 },
#         title=f'Mortality Rate vs Oil Consumption and GDP per capita in {year}',
#     ).update_layout(
#         xaxis=dict(range=[-df["Mortality Rate"].max() * 0.2, df["Mortality Rate"].max() * 1.1]),
#         yaxis=dict(range=[-df["Oil Consumption per capita (tonnes per year)"].max() * 0.2, df["Oil Consumption per capita (tonnes per year)"].max() * 1.1]),
#         margin=dict(l=20, r=20, t=30, b=20),
#         font=dict(size=12),
#         coloraxis_showscale=False
#     ).update_traces(
#         contours_coloring="fill",
#         coloraxis="coloraxis1",
#         contours_showlabels = False,
#         colorscale="Viridis",
#         showlegend=False
#     )

def create_density_contour_fig(year, continents):
    mask = (df["Continent"].isin(continents) & (df["Year"] == year))
    filtered_df = df.loc[mask]
    filtered_df.loc[:, 'log_GDP'] = np.log(filtered_df['GDP per capita (US$)'])
    
    gdp_levels = [20, 40, 60, 80]
    
    colors = ['#648fff', '#785ef0', '#dc267f', '#fe6100', '#ffb000']
    
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
            x=continent_df["Mortality Rate"],
            y=continent_df["Oil Consumption per capita (tonnes per year)"],
            z=continent_df["GDP per capita (US$)"],
            histfunc="sum",
            histnorm="percent",
            colorscale=colors,
            autocontour=False,
            contours_coloring="fill",
            line=dict(width=1),
            hovertemplate="Mortality Rate: %{x}<br>Oil Consumption: %{y}<br>GDP per capita: %{z}<extra></extra>",
            showscale=True,
            contours=dict(
                start=min(gdp_levels),
                end=max(gdp_levels),
                size=(max(gdp_levels) - min(gdp_levels)) / len(gdp_levels),
            ),
            colorbar=dict(
                title="GDP per capita (%)",
                tickvals=gdp_levels,
                ticktext=["Low (20 %)", "Medium (40 %)", "High (60 %)", "Very High (80 %)"],
            ),
        )

        fig.add_trace(hist2d_contour, row=1, col=i)
        fig.update_xaxes(title_text="Mortality Rate", title_standoff=5, range=[-50, 500], title_font_size=14, row=1, col=i)
        fig.update_yaxes(title_text="Oil Consumption per<br>capita (tonnes per year)", title_standoff=0, title_font_size=14, range=[-5, 15], row=1, col=i)

    fig.update_layout(
        title=f'Mortality Rate vs Oil Consumption and GDP per capita in {year}',
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(size=12),
        coloraxis_showscale=False
    )

    return fig


def create_scatter_fig(year, continents):
    mask = (df["Continent"].isin(continents) & (df["Year"] == year))
    return px.scatter(
        df.loc[mask],
        x="Mortality Rate",
        y="Oil Consumption per capita (tonnes per year)",
        size="GDP per capita (US$)",
        color="Continent",
        hover_name="Country",
        labels={
                    "Oil Consumption per capita (tonnes per year)": "Oil Consumption per capita<br>(tonnes per year)",
                    "Country": "Country",
                    "Continent": "Continent",
                    "Mortality Rate": "Mortality Rate (per 1000 births)",
                },
        log_x=False,
        size_max=55,
        title=f'Mortality Rate vs Oil Consumption per capita in {year}',
    ).update_layout(
        xaxis=dict(range=[-df["Mortality Rate"].max() * 0.2, df["Mortality Rate"].max() * 1.1]),
        yaxis=dict(range=[-df["Oil Consumption per capita (tonnes per year)"].max() * 0.2, df["Oil Consumption per capita (tonnes per year)"].max() * 1.1]),
        margin=dict(l=20, r=20, t=30, b=20),
        font=dict(size=12)
    )

def create_mortality_bar_fig(year, continents):
    mask = (df["Continent"].isin(continents) & (df["Year"] == year))
    top_10 = df[mask].nlargest(10, 'Mortality Rate')
    top_10.reset_index(drop=True, inplace=True)
    
    fig = px.bar(
        top_10,
        x="Mortality Rate",
        y="Country",
        color="Continent",
        labels={
                    "Oil Consumption per capita (tonnes per year)": "Oil Consumption per capita<br>(tonnes per year)",
                    "Country": "Country",
                    "Continent": "Continent",
                    "Mortality Rate": "Mortality Rate (per 1000 births)",
                },
        orientation='h',
        title=f'Top 10 Countries by Mortality Rate in {year}',
        color_discrete_map={'Asia': '#648fff', 'Europe': '#785ef0', 'Africa': '#dc267f', 'North America': '#fe6100', 'South America': '#ffb000', 'Oceania': '#054fb9'}
    )
    fig.update_layout(
        xaxis=dict(range=[0, df["Mortality Rate"].max() * 1.1]),
        yaxis=dict(categoryorder='total ascending'),
        margin=dict(l=20, r=20, t=30, b=20),
        font=dict(size=12),
        xaxis_autorange=False,
        yaxis_autorange=True
    )

    return fig

def create_oil_bar_fig(year, continents):
    mask = (df["Continent"].isin(continents) & (df["Year"] == year))
    top_10 = df[mask].nlargest(10, 'Oil Consumption per capita (tonnes per year)')
    top_10.reset_index(inplace=True)
    return px.bar(
        top_10,
        x="Oil Consumption per capita (tonnes per year)",
        y="Country",
        color="Continent",
        labels={
                    "Oil Consumption per capita (tonnes per year)": "Oil Consumption per capita<br>(tonnes per year)",
                    "Country": "Country",
                    "Continent": "Continent",
                    "Mortality Rate": "Mortality Rate (per 1000 births)",
                },
        orientation='h',
        title=f'Top 10 Countries by Oil Consumption in {year}',
        color_discrete_map={'Asia': '#648fff', 'Europe': '#785ef0', 'Africa': '#dc267f', 'North America': '#fe6100', 'South America': '#ffb000', 'Oceania': '#054fb9'}
    ).update_layout(
        xaxis=dict(range=[0, df["Oil Consumption per capita (tonnes per year)"].max() * 1.01]),
        yaxis=dict(categoryorder='total ascending'),
        margin=dict(l=20, r=20, t=30, b=20),
        font=dict(size=12),
        xaxis_autorange=False,
        yaxis_autorange=True
    )

def create_gdp_bar_fig(year, continents):
    mask = (df["Continent"].isin(continents) & (df["Year"] == year))
    top_10 = df[mask].nlargest(10, 'GDP per capita (US$)')
    top_10.reset_index(inplace=True)
    return px.bar(
        top_10,
        x="GDP per capita (US$)",
        y="Country",
        color="Continent",
        orientation='h',
        labels={
                    "Oil Consumption per capita (tonnes per year)": "Oil Consumption per capita<br>(tonnes per year)",
                    "Country": "Country",
                    "Continent": "Continent",
                    "Mortality Rate": "Mortality Rate (per 1000 births)",
                },
        title=f'Top 10 Countries by GDP in {year}',
        color_discrete_map={'Asia': '#648fff', 'Europe': '#785ef0', 'Africa': '#dc267f', 'North America': '#fe6100', 'South America': '#ffb000', 'Oceania': '#054fb9'}
    ).update_layout(
        xaxis=dict(range=[0, df["GDP per capita (US$)"].max() * 1.01]),
        yaxis=dict(categoryorder='total ascending'),
        margin=dict(l=20, r=20, t=30, b=20),
        font=dict(size=12),
        xaxis_autorange=False,
        yaxis_autorange=True
    )

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
                    style={'width': '33%', 'height': '275px', 'display': 'inline-block', 'margin': '0px', 'padding': '0px'}, 
                    figure=create_mortality_bar_fig(df["Year"].min(), df["Continent"].unique().tolist())
                ),
                dcc.Graph(
                    id="graph-with-slider2",
                    style={'width': '33%', 'height': '275px', 'display': 'inline-block', 'margin': '0px', 'padding': '0px'}, 
                    figure=create_oil_bar_fig(df["Year"].min(), df["Continent"].unique().tolist())
                ),
                dcc.Graph(
                    id="graph-with-slider4",
                    style={'width': '33%', 'height': '275px', 'display': 'inline-block', 'margin': '0px', 'padding': '0px'}, 
                    figure=create_gdp_bar_fig(df["Year"].min(), df["Continent"].unique().tolist())
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
    Output("graph-with-slider4", "figure"),
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
        create_gdp_bar_fig(year, continents),
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
