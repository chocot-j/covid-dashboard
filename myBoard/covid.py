import requests
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

from datetime import datetime
from plotly.offline import plot
from keys import ENCODING_KEY, DECODING_KEY


URL = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson'
ENCODING_KEY = ENCODING_KEY
DECODING_KEY = DECODING_KEY

def get_data():
    today = datetime.now().date().strftime('%Y%m%d')
    params ={'serviceKey': DECODING_KEY, 'startCreateDt': 20200101, 'endCreateDt': today}   
    response = requests.get(URL, params=params)
    df = pd.read_xml(response.content, xpath='//item')

    return df


df = get_data()
df_2022 = df[df['stateDt'] > 20220101].copy()
df_2022['date'] = df_2022['createDt'].apply(lambda x: x[:10])


def deathCnt_plot():
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_2022['date'], y=df_2022['deathCnt'],
        mode='lines', 
        line=dict(width=2, color='#A5C9CA'), 
        fill='tozeroy',
        fillcolor='rgba(231, 246, 242, .5)'))
    fig.update_layout(
        template='plotly_white',
        width=560, height=300,
        margin=dict(l=0, r=0, t=0, b=0))
    return plot(fig, output_type='div')


def decideCnt_plot():
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_2022['date'], y=df_2022['decideCnt'],
        mode='lines', 
        line=dict(width=2, color='#A5C9CA'), 
        fill='tozeroy',
        fillcolor='rgba(231, 246, 242, .5)'))
    fig.update_layout(
        template='plotly_white',
        width=560, height=300,
        margin=dict(l=0, r=0, t=0, b=0))
    return plot(fig, output_type='div')
