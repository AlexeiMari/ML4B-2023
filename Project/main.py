#Hier werden schon Mal die wichtigsten Libs, die wir verwenden werden, importiert.
#Geht sicher, dass ihr die installiert habt
import pandas as pd
import streamlit as st
import csv
import sklearn
import numpy as np
import json
import torch
import math
import os
import tsfresh

### Attributes
#knn = torch.load(r"..\Models" + "\\" + "KNN (hpo)_2023-06-02")
#rnf = torch.load(r"..\Models" + "\\" + "RNF_2023-06-02")

#Don't touch this! The List has to be identical to the list in the notebook
sensors = ["Accelerometer","Location","Orientation"]

### Functions
def process_data(file):
    return None

def transform_data_csv(file):
    datasets = {}  # Ein Dictionary
    for sensor in sensors:
        # Dataframe wird eingelesen
        df = pd.read_csv(file + "\\" + sensor + ".csv")

        # Zeittransformation
        # df["time"] = pd.to_datetime(df['time'], unit = 'ns')
        # df["Readable_Time"] = df["time"]
        # for i in range(0,len(df["time"])):
        #    df["Readable_Time"][i] = df["time"][i].to_pydatetime()
        df = df.drop(columns=["time"])
        df = df.dropna(axis=1)

        # Datenschutz. Falls Location ein Sensor ist, wird davon nur die Speed verwendet
        if (sensor == "Location"):
            df = df.drop(columns=df.columns.difference(["speed", "Readable_Time", "seconds_elapsed"]))

        elif sensor == "Accelerometer":
            df["Magnitude(acc)"] = np.sqrt(df["x"] ** 2 + df["y"] ** 2 + df["z"] ** 2)
            df = df.drop(columns=df.columns.difference(["Magnitude(acc)", "Readable_Time", "seconds_elapsed"]))
        # df["activity"] = action #Darf hier nicht gesetzt werden, ist aber im Dicitonary vermerkt
        df["ID"] = file

        # Dataframe wird dem Dictionay hinzugefügt
        datasets[sensor] = df

    return datasets


def transform_data_json(file):
    datasets = {}  # Ein Dictionary

    df = pd.read_json(file)

    # Zeittransformation
    # df["time"] = pd.to_datetime(df['time'], unit = 'ns')
    ##df["Readable_Time"] = df["time"]
    # for i in range(0,len(df["time"])):
    #    df["Readable_Time"][i] = df["time"][i].to_pydatetime()
    df = df.drop(columns=["time"])

    for sensor in sensors:
        temp = df.loc[df["sensor"] == sensor]
        temp = temp.dropna(axis=1)
        temp = temp.drop(columns=["sensor"])
        # Datenschutz. Falls Location ein Sensor ist, wird davon nur die Speed verwendet
        if (sensor == "Location"):
            temp = temp.drop(columns=temp.columns.difference(["speed", "Readable_Time", "seconds_elapsed"]))

        elif sensor == "Accelerometer":
            temp["Magnitude(acc)"] = np.sqrt(temp["x"] ** 2 + temp["y"] ** 2 + temp["z"] ** 2)
            temp = temp.drop(columns=temp.columns.difference(["Magnitude(acc)", "Readable_Time", "seconds_elapsed"]))

        # temp["activity"] = action #Darf hier nicht gesetzt werden, ist aber im Dicitonary vermerkt
        temp["ID"] = file

        # Dataframe wird dem Dictionary hinzugefügt
        datasets[sensor] = temp

    return datasets

### Pythonic Area

st.title("Mobility Classification App")

uploaded_file = st.file_uploader("Please upload a sensor data file. JSON or .zip containing CSVs are allowed")

