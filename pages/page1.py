### mock data
import random
import pandas as pd
import streamlit as st
import numpy as np
import json
import torch
import plotly.express as px
import math
import os
import tsfresh
import zipfile as zf
from tqdm.auto import tqdm

activities = ['Laufen', 'Idle', 'Auto', 'U-Bahn', 'Fahrrad']
minutes_range = (5, 15)  # Bereich der Minuten für jede Aktivität

data = {'Aktivität': []}

for activity in activities:
    minutes = random.randint(minutes_range[0], minutes_range[1])
    data['Aktivität'].extend([activity] * minutes)
df = pd.DataFrame(data)
#st.dataframe(df)
###
#
activity_filter = st.selectbox("Select the Activity", pd.unique(df["Aktivität"]))
df_selection = df[df["Aktivität"] == activity_filter]
if activity_filter == 'Laufen':
    bar_laufen = px.bar(
    df_selection,
    x='Aktivität',
    orientation='v',
    title='Aktivitäten',
    color_discrete_sequence=['#2ECC71'],
    template='plotly_white'
    )
    st.plotly_chart(bar_laufen)
elif activity_filter == 'Idle':
    bar_idle = px.bar(
    df_selection,
    x='Aktivität',
    orientation='v',
    title='Aktivitäten',
    color_discrete_sequence=['#2ECC71'],
    template='plotly_white'
    )
    st.plotly_chart(bar_idle)
elif activity_filter == 'U-Bahn':
    bar_ubahn = px.bar(
    df_selection,
    x='Aktivität',
    orientation='v',
    title='Aktivitäten',
    color_discrete_sequence=['#2ECC71'],
    template='plotly_white'
    )
    st.plotly_chart(bar_ubahn)
elif activity_filter == 'Auto':
    bar_auto = px.bar(
    df_selection,
    x='Aktivität',
    orientation='v',
    title='Aktivitäten',
    color_discrete_sequence=['#2ECC71'],
    template='plotly_white'
    )
    st.plotly_chart(bar_auto)
elif activity_filter == 'Fahrrad':
    bar_fahrrad = px.bar(
    df_selection,
    x='Aktivität',
    orientation='v',
    title='Aktivitäten',
    color_discrete_sequence=['#2ECC71'],
    template='plotly_white'
    )
    st.plotly_chart(bar_fahrrad)

if not activity_filter == 'Laufen' or 'Idle' or 'U-Bahn' or 'Auto' or 'Fahrrad':
    bar = px.bar(
        df,
        x='Aktivität',
        orientation='v',
        title='Aktivitäten',
        color_discrete_sequence=['#2ECC71'],
        template='plotly_white'
    )

    st.plotly_chart(bar)
