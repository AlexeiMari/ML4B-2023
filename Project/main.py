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
import pickle
import zipfile as zf

### Attributes

#knn = torch.load(r"..\Models\KNN (hpo)_2023-06-02")
#rnf = torch.load(r"..\Models" + "\\" + "RNF_2023-06-02")

#Rene Workaround
knn = torch.load(r"C:\Users\ReneJ\Desktop\UnityStuff\ML4B-2023\Project\Models\KNN (hpo)_2023-06-02")
rnf = torch.load(r"C:\Users\ReneJ\Desktop\UnityStuff\ML4B-2023\Project\Models\RNF_2023-06-02")

#Don't touch this! The List has to be identical to the list in the notebook
sensors = ["Accelerometer","Location","Orientation"]

### Functions
def process_data(upload):
    data = None
    if zf.is_zipfile(upload): #Hochgeladene Datei ist eine zip mit CSVs drinnen
        st.write("Is ne zip")
        file = None
        extr_dir = r"C:\Users\ReneJ\Desktop\UnityStuff\ML4B-2023\Project\uploaded_files"

        with zf.ZipFile(upload, 'r') as zip_ref:
            zip_ref.extractall(extr_dir)

        for f in os.listdir(extr_dir):
            file = f

        data = transform_data_csv(extr_dir + "\\" + file)
        st.write(extr_dir + "\\" + file)

    else: #Hochgeladene Datei ist eine JSON
        st.write("Is ne json")
        x = upload.getvalue()
        #st.write(x)
        x_json = x.decode('utf8')
        data = json.loads(x_json)
        #st.write(s)
        with open(r"C:\Users\ReneJ\Desktop\UnityStuff\ML4B-2023\Project\json.json", 'w') as j:
            json.dump(data,j)
        data = transform_data_json(r"C:\Users\ReneJ\Desktop\UnityStuff\ML4B-2023\Project\json.json")

    st.write(data)
    return data

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

### Streamlit Area
st.set_page_config(page_title="Mobility Classification App", page_icon=":oncoming_automobile:", layout="wide")

st.subheader("Lets classify your mobility!")
st.write("First we need some Input from you")
#uploaded_file = st.file_uploader("Please upload a sensor data file. JSON or .zip containing CSVs are allowed")
#knn = torch.load(r"..\Models" + "\\" + "KNN (hpo)_2023-06-02")
def main():
    uploaded_file = st.file_uploader("Please upload a sensor data file. JSON or .zip containing CSVs are allowed", accept_multiple_files=False)
    if st.button("Classify me!"):
        process_data(uploaded_file)
        def classify_temperature(temperature):
            if temperature >= 20:
                return "T-Shirt"
            elif temperature >= 10:
                return "Pullover"
            else:
                return "Jacke"
        input_temperature = 20
        classify_temperature = classify_temperature(input_temperature)
        st.write("The prediction is: ", classify_temperature)
if __name__ == "__main__":
    main()


