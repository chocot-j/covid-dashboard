from __future__ import annotations
import requests, json
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

from datetime import datetime
from plotly.offline import plot
from keys import API_KEY


URL_ALL = 'https://api.corona-19.kr/korea/beta'
URL_VAC = 'https://api.corona-19.kr/korea/vaccine'
API_KEY = API_KEY

'''
totalCnt: 국내 확진자 수
recCnt: 국내 완치자 수
dathCnt: 국내 사망자 수
isolCnt: 국내 격리자 수
qurRate: 코로나 발생률
incDec: 전일대비 확진
incDecK: 전일대비 확진(국내)
incDecF: 전일대비 확진(해외)
'''
params ={'serviceKey': API_KEY}   
response = requests.get(URL_ALL, params=params).json()
res_info = response.pop('API')
df = pd.DataFrame.from_dict(response).transpose().rename_axis("state").reset_index()
df = pd.concat([df[list(df.columns.values)[:2]], df[list(df.columns.values)[2:]].astype('int')], axis=1)

response2 = requests.get(URL_VAC, params=params).json()
res2_info = response2.pop('API')
df2 = pd.DataFrame.from_dict(response2).transpose().rename_axis("state").reset_index()
vac1 = pd.DataFrame(df2['vaccine_1'].values.tolist())
vac2 = pd.DataFrame(df2['vaccine_2'].values.tolist())
vac3 = pd.DataFrame(df2['vaccine_3'].values.tolist())
vac4 = pd.DataFrame(df2['vaccine_4'].values.tolist())
df_vac = pd.concat([df2[['state']], vac1, vac2, vac3, vac4], axis=1)

def stateRank_plot():
    df_qurRate = df.iloc[1:-1][['state', 'qurRate']].sort_values(by=['qurRate'])
    df_qurRate['annotation'] = df_qurRate['qurRate'].apply(lambda x: str(round(x/1000, 1)) + 'k')

    fig = go.Figure(go.Bar(
        x=df_qurRate['qurRate'],
        y=df_qurRate['state'],
        orientation='h'
    ))

    annotations = []
    for y, x, text in df_qurRate.values:
        annotations.append(dict(
            x=x-3000, y=y,
            xref='x', yref='y',
            text=text,
            font=dict(color='white', size=12),
            showarrow=False,
            ))
    fig.update_layout(annotations=annotations)
    fig.update_layout(
        width=500, height=400,
        template='plotly_white',
        font=dict(size=13),
        margin=dict(l=0, r=0, t=0, b=0))
    return plot(fig, output_type='div')


def map_plot():
    df_qurRate = df.iloc[1:-1][['state', 'qurRate']].reset_index(drop=True)
    state_geo = json.load(open('static\others\TL_SCCO_CTPRVN.json', encoding='utf-8'))
    state_match = {
        'busan':'Busan',
        'chungbuk':'Chungcheongbuk-do',
        'chungnam':'Chungcheongnam-do',
        'daegu':'Daegu',
        'daejeon':'Daejeon',
        'gangwon':'Gangwon-do',
        'gwangju':'Gwangju',
        'gyeonggi':'Gyeonggi-do',
        'gyeongbuk':'Gyeongsangbuk-do',
        'gyeongnam':'Gyeongsangnam-do',
        'incheon':'Incheon',
        'jeju':'Jeju-do',
        'jeonnam':'Jellanam-do',
        'jeonbuk':'Jeollabuk-do',
        'sejong':'Sejong-si',
        'seoul':'Seoul',
        'ulsan':'Ulsan',
        }
    df_qurRate['CTP_ENG_NM'] = df_qurRate['state'].apply(lambda x: state_match[x])
    df_qurRate['log_qurRate'] = df_qurRate['qurRate'].apply(np.log10)
    fig = px.choropleth(
        df_qurRate, geojson=state_geo,
        locations='CTP_ENG_NM',
        featureidkey='properties.CTP_ENG_NM',
        color='log_qurRate',
        color_continuous_scale='GnBu',
        scope='asia',
        center={'lat':35.565, 'lon':127.986},
        hover_name='state',
        hover_data=['qurRate']
        )
    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0))
    fig.update_coloraxes(colorbar=dict(len=0.7, x=0.8))
    return plot(fig, output_type='div')


def totalCnt_plot():
    df_totalCnt = df.iloc[1:-1][['state', 'totalCnt']].reset_index(drop=True)
    labels = df_totalCnt['state']
    values = df_totalCnt['totalCnt']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker=dict(colors=px.colors.sequential.Teal))])
    fig.update_layout(
        annotations=[dict(
            x=0.5, y=0.5,
            xref='paper', yref='paper',
            text=f"Total<br> {df.iloc[0]['totalCnt']}",
            font=dict(color='#2B2B2B', size=14),
            showarrow=False,
        )],
        width=400, height=300,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    fig.update_layout(legend=dict(x=1.3))
    return plot(fig, output_type='div')


def covid_incDec():
    incDec_list = df.iloc[0][['incDec', 'incDecK', 'incDecF']].tolist()
    return incDec_list


def vaccine_plot():
    df_vac_total = df_vac.iloc[0]
    col_keys = df_vac_total.keys().tolist()
    vac_new = list(filter(lambda x: 'new' in x, col_keys))
    vac_old = list(filter(lambda x: 'old' in x, col_keys))
    df_vaccine = pd.DataFrame(
        {
            'vaccine':['vaccine_1', 'vaccine_2', 'vaccine_3', 'vaccine_4'],
            'vaccine_new':df_vac_total[vac_new].values.tolist(), 
            'vaccine_old':df_vac_total[vac_old].values.tolist()})

    df_vaccine['total'] = df_vaccine['vaccine_new'] + df_vaccine['vaccine_old']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_vaccine['vaccine'], y=df_vaccine['total'],
        marker_color='#A5C9CA', marker_line_color='#395B64',
        marker_line_width=1.5, opacity=0.6, width=0.5))
    fig.add_trace(go.Scatter(
        x=df_vaccine['vaccine'], y=df_vaccine['total'], 
        mode='lines+markers', 
        marker=dict(size=10, color='#CEE5D0', line=dict(color='#94B49F', width=2)),
        line=dict(color='#94B49F', dash='dot')),
        )
    fig.update_traces(showlegend=False)
    fig.update_layout(
        template='plotly_white',
        width=400, height=300,
        margin=dict(l=0, r=0, t=0, b=0))
    return plot(fig, output_type='div')
