import pandas as pd

data = pd.read_csv('netflix_titles.csv', index_col=0)

data['country']

num_countries = []

all_countries = []

for i in data['country'].astype(str):
    if i == 'nan':
        continue
    else:
        for m in i.split(', '):

            num_countries.append(m)
for i in num_countries:
    i = i.replace(',','')
    all_countries.append(i)
# print(all_countries)
all_countries = pd.Series(all_countries)
unique_countries = all_countries.unique()

all_countries.describe()
num_media_by_country = all_countries.value_counts().astype(float)
num_media_by_country = pd.DataFrame(num_media_by_country)
num_media_by_country = num_media_by_country.rename(columns={0:'Count'})
num_media_by_country = num_media_by_country.reset_index().rename(columns={'index':'Countries'})

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
c = df.drop('GDP (BILLIONS)',axis=1)
c = c.rename(columns={'COUNTRY':'Countries'})
country_with_code = pd.merge(num_media_by_country,c,on='Countries',how='left')


import plotly.graph_objects as go
import pandas as pd
fig = go.Figure(data=go.Choropleth(
    locations = country_with_code['CODE'],
    z = country_with_code['Count'],
    text = 'Total Media Available',
    colorscale = 'Thermal',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    #colorbar_tickprefix = ,
    colorbar_title = 'Total Media',
))
fig.update_layout(
    title_text='Netflix Movies and TV Shows',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://www.kaggle.com/shivamb/netflix-shows">\
            Netflix Movies and TV Shows - 2019 </a>',
        showarrow = False
    )]
)
fig.show()