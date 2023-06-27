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
import matplotlib.pyplot as plt
import plotly.graph_objects as go
st.set_page_config(page_title="Mobility Classification App", page_icon=":oncoming_automobile:", layout="wide")
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

bar = px.bar(
    df,
    x='Aktivität',
    orientation='v',
    title='Aktivitäten',
    color='Aktivität',
    color_discrete_sequence=['#3D7A3F', '#EB7A27', '#B4393C', '#FBB024', '#7A5803'],
    template='plotly_white'
    )
bar.update_layout(
    plot_bgcolor='#282C34',
    paper_bgcolor='#282C34',
    height=300,
    width=500,
)
st.plotly_chart(bar)
prediction_data = {
    0: {
        0: "walk",
        1: 20
    },
    1: {
        0: "bike",
        1: 15
    },
    2: {
        0: "car",
        1: 3
    },
    3: {
        0: "bike",
        1: 15
    },
    4: {
        0: "ubahn",
        1: 9
    },
    5: {
        0: "walk",
        1: 45
    },
    6: {
        0: "ubahn",
        1: 2
    },
    7: {
        0: "bike",
        1: 5
    },
    8: {
        0: "walk",
        1: 3
    },
    9: {
        0: "idle",
        1: 50
    }
}

# Extrahieren der Aktivitäten und Häufigkeiten aus dem JSON
aktivitaeten = [prediction_data[key][0] for key in prediction_data]
haeufigkeiten = [prediction_data[key][1] for key in prediction_data]

# Aktivitäten und Farben
farben = ['#3D7A3F', '#EB7A27', '#B4393C', '#FBB024', '#7A5803']

# Dictionary zur Zuordnung von Aktivitäten zu Farben
aktivitaeten_farben = {}
startfarbe_index = 0

# Erstellen der Figure und Axes
fig2, ax = plt.subplots(figsize=(6, 1))
fig2.set_facecolor('#282C34')

# Schleife über die Aktivitäten
startpunkt = 0
bar_hoehe = 0.01

# Liste für die Legendenbeschriftungen und zugehörige Farben
legenden_beschriftungen = []
legenden_farben = []

for idx, aktivitaet in enumerate(aktivitaeten):
    # Überprüfen, ob die Aktivität bereits im Dictionary vorhanden ist
    if aktivitaet in aktivitaeten_farben:
        farbe = aktivitaeten_farben[aktivitaet]
    else:
        # Falls die Aktivität noch keine Farbe hat, die nächste Farbe auswählen
        farbe = farben[startfarbe_index % len(farben)]
        startfarbe_index += 1
        aktivitaeten_farben[aktivitaet] = farbe
    
    # Zählen der Häufigkeit der Aktivität
    haeufigkeit = haeufigkeiten[idx]
    
    # Anzahl der Aktivitäten innerhalb des Balkens
    ax.text(startpunkt + haeufigkeit / 2, bar_hoehe + 0.005, str(haeufigkeit), ha='center', va='bottom', color='white', fontsize=6)

    # Einfärben des Strahls entsprechend der Häufigkeit
    ax.bar(startpunkt, bar_hoehe, width=haeufigkeit, color=farbe, align='edge')
    
    # Überprüfen, ob die Aktivität bereits in der Legendenliste vorhanden ist
    if aktivitaet not in legenden_beschriftungen:
        # Hinzufügen der Aktivitätsbeschreibung zur Legendenliste
        legenden_beschriftungen.append(aktivitaet)
        legenden_farben.append(farbe)

    # Aktualisierung des Startpunkts für die nächste Aktivität
    startpunkt += haeufigkeit

# Anpassung der Achsen
ax.set_xlim(0, startpunkt)
ax.set_ylim(0, 0)
ax.axis('off')

legende_handles = [plt.Rectangle((0, 0), 1, 1, color=farbe) for farbe in legenden_farben]

# Anzeigen der Legende mit den korrekten Farben
ax.legend(legende_handles, legenden_beschriftungen, loc='center', bbox_to_anchor=(0.5, -0.2), ncol=len(legenden_beschriftungen), labelcolor='white', facecolor='#282C34', edgecolor='#282C34', fontsize=6)


st.pyplot(fig2)

def berechne_kalorien_bike(json_data, aktivitaet):
    kalorien_verbrauch = 0
    for key, value in json_data.items():
        if value[0] == aktivitaet:
            minuten = value[1]
            kalorien_verbrauch += minuten * 6
    return kalorien_verbrauch

def berechne_kalorien_walk(json_data, aktivitaet):
    kalorien_verbrauch = 0
    for key, value in json_data.items():
        if value[0] == aktivitaet:
            minuten = value[1]
            kalorien_verbrauch += minuten * 4
    return kalorien_verbrauch


verbrauchte_kalorien_bike = berechne_kalorien_bike(prediction_data, "bike")
verbrauchte_kalorien_walk = berechne_kalorien_walk(prediction_data, "walk")
st.markdown("## Kalorienverbrauch", unsafe_allow_html=True)
st.markdown(
    f'<div style="background-color: #282C34; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 10px; border-radius: 5px; height: 150px; width:150px;">'
    f'<div style="color: white; font-weight: bold; text-align: center;">Kalorien</div>'
    f'<div style="color: white; font-size: 24px; text-align: center;">{verbrauchte_kalorien_bike + verbrauchte_kalorien_walk}</div>'
    '</div>',
    unsafe_allow_html=True
)



activities = ['Laufen', 'Idle', 'Auto', 'U-Bahn', 'Fahrrad']
minutes_range = (5, 15)  # Bereich der Minuten für jede Aktivität

data = {'Aktivität': []}

for activity in activities:
    minutes = random.randint(minutes_range[0], minutes_range[1])
    data['Aktivität'].extend([activity] * minutes)

df = pd.DataFrame(data)

# Prozentsatz der Aktivitäten berechnen
activity_counts = df['Aktivität'].value_counts()
activity_percentages = activity_counts / activity_counts.sum() * 100

fig_pie = px.pie(df, names='Aktivität', title='Verteilung der Aktivitäten')
fig_pie.update_traces(textposition='inside', textinfo='percent+label')

# Größe des Tortendiagramms anpassen
fig_pie.update_layout(
    height=500,
    width=500,
    plot_bgcolor='#282C34',
    paper_bgcolor='#282C34',
    font=dict(color='white')
)
st.plotly_chart(fig_pie)