#Hier werden schon Mal die wichtigsten Libs, die wir verwenden werden, importiert.
#Geht sicher, dass ihr die installiert habt
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
import matplotlib.pyplot as plt
from stqdm import stqdm

st.set_page_config(page_title="Mobility Classification App", page_icon=":oncoming_automobile:", layout="wide")

### Attributes
local = False
if not local:
    knn = torch.load(r"KNN")
    gbc = torch.load(r"GBC_2023-06-22")


#Rene Workaround
if local:
    #knn = torch.load(r"C:\Users\ReneJ\Desktop\UnityStuff\ML4B-2023\Project\Models\KNN (hpo)_2023-06-02")
    gbc = torch.load(r"C:\Users\ReneJ\Desktop\UnityStuff\ML4B-2023\GBC_2023-06-22")

#Don't touch this! The List has to be identical to the list in the notebook
sensors = ["Accelerometer","Location","Orientation"]

### Functions
def process_data(upload):
    data = None
    if zf.is_zipfile(upload): #Hochgeladene Datei ist eine zip mit CSVs drinnen
        st.write("Is ne zip")
        file = None
        if local:
            extr_dir = r"C:\Users\ReneJ\Desktop\UnityStuff\ML4B-2023\uploaded_files"
        if not local:
            extr_dir = r"uploaded_files"

        with zf.ZipFile(upload, 'r') as zip_ref:
            zip_ref.extractall(extr_dir)

        for f in os.listdir(extr_dir):
            file = f
            st.write(f)

        st.write(extr_dir)
        if local:
            data, gps = transform_data_csv(extr_dir + "\\" + file)
        if not local:
            st.write(str(os.getcwd()))
            cwd = os.getcwd()
            data, gps = transform_data_csv(extr_dir)
        st.write(extr_dir + "\\" + file)

    else: #Hochgeladene Datei ist eine JSON
        st.write("Is ne json")
        x = upload.getvalue()
        #st.write(x)
        x_json = x.decode('utf8')
        data = json.loads(x_json)
        #st.write(s)

        if local:
            json_path = r"C:\Users\ReneJ\Desktop\UnityStuff\ML4B-2023\json.json"
        if not local:
            json_path = r"json.json"

        with open(json_path, 'w') as j:
            json.dump(data,j)
        data, gps = transform_data_json(json_path)

    #st.write(data)
    splitData = split_data([data], 1)
    metrics = calculate_features(splitData)
    end = combine(metrics)

    prediction = gbc.predict(end)

    timeLineData = create_time_line_data(prediction)
    tupelList = time_line_data_to_tupel(timeLineData)
    return tupelList, gps, end, prediction

def transform_data_csv(file):
    datasets = {}  # Ein Dictionary
    gps = None
    for sensor in sensors:
        # Dataframe wird eingelesen
        st.write(file)

        path = os.path.join(file, sensor)
        st.write(path)
        df = pd.read_csv(path + ".csv")

        # Zeittransformation
        # df["time"] = pd.to_datetime(df['time'], unit = 'ns')
        # df["Readable_Time"] = df["time"]
        # for i in range(0,len(df["time"])):
        #    df["Readable_Time"][i] = df["time"][i].to_pydatetime()
        df = df.drop(columns=["time"])
        df = df.dropna(axis=1)

        # Datenschutz. Falls Location ein Sensor ist, wird davon nur die Speed verwendet
        if (sensor == "Location"):
            gps = df
            df = df.drop(columns=df.columns.difference(["speed", "Readable_Time", "seconds_elapsed"]))

        elif sensor == "Accelerometer":
            df["Magnitude(acc)"] = np.sqrt(df["x"] ** 2 + df["y"] ** 2 + df["z"] ** 2)
            df = df.drop(columns=df.columns.difference(["Magnitude(acc)", "Readable_Time", "seconds_elapsed"]))
        # df["activity"] = action #Darf hier nicht gesetzt werden, ist aber im Dicitonary vermerkt
        df["ID"] = file

        # Dataframe wird dem Dictionay hinzugefügt
        datasets[sensor] = df

    return datasets, gps


def transform_data_json(file):
    datasets = {}  # Ein Dictionary
    gps = None

    df = pd.read_json(file)

    df = df.drop(columns=["time"])

    for sensor in sensors:
        temp = df.loc[df["sensor"] == sensor]
        temp = temp.dropna(axis=1)
        temp = temp.drop(columns=["sensor"])
        # Datenschutz. Falls Location ein Sensor ist, wird davon nur die Speed verwendet
        if (sensor == "Location"):
            gps = temp
            temp = temp.drop(columns=temp.columns.difference(["speed", "Readable_Time", "seconds_elapsed"]))

        elif sensor == "Accelerometer":
            temp["Magnitude(acc)"] = np.sqrt(temp["x"] ** 2 + temp["y"] ** 2 + temp["z"] ** 2)
            temp = temp.drop(columns=temp.columns.difference(["Magnitude(acc)", "Readable_Time", "seconds_elapsed"]))

        # temp["activity"] = action #Darf hier nicht gesetzt werden, ist aber im Dicitonary vermerkt
        temp["ID"] = file

        # Dataframe wird dem Dictionary hinzugefügt
        datasets[sensor] = temp

    return datasets, gps

def split_data(list, length_of_time_series):
    splitted_list = []
    for dict in list:
        amount_of_splits = 999999999999
        print(dict["Accelerometer"].iloc[-1]["ID"])
        # print(dict)
        for sensor in sensors:
            temp_aos = math.floor(dict[sensor]["seconds_elapsed"].iloc[-1] / (60 * length_of_time_series))
            if temp_aos < amount_of_splits:
                amount_of_splits = temp_aos
        print(amount_of_splits)
        if amount_of_splits == 999999999999 or amount_of_splits <= 1:  # case 1: Something went wrong, we don't split. Case 2: The Timeseries is not long enough to be splited
            # Wenn der Datensatz zu kurz zum splitten ist, wird er nicht gesplittet, stattdessen wird er einfach als ganzes in die splitted_list gelegt
            splitted_list.append(dict)

        else:
            split_dict = {}  # Dieses dictionary wird jedem Sensor eine Liste von aufgesplitteten DFs zuweisen
            for sensor in sensors:
                splitted_dict_entry = np.array_split(dict[sensor],
                                                     amount_of_splits)  # Das ist jetzt ne Liste mit aufgeteilten Dataframes
                print(len(splitted_dict_entry))
                id_suffix = 0
                for df in splitted_dict_entry:
                    df["ID"] = df["ID"] + "_" + str(id_suffix)
                    id_suffix += 1

                split_dict[sensor] = splitted_dict_entry

            for i in range(0, amount_of_splits):
                sub_dict = {}
                for sensor in sensors:
                    sub_dict[sensor] = split_dict[sensor][i]
                splitted_list.append(sub_dict)

    return splitted_list


def calculate_features(input_list):
    ff_list = []

    def rms(df):
        square = df ** 2
        square = square.sum()
        mean = (square / len(df))
        root = math.sqrt(mean)
        return root


    for dict in stqdm(input_list):
        #print((list(dict.keys())[1] == "Accelerometer") and (list(dict.keys())[2] == "Location") and (
        #            list(dict.keys())[3] == "Orientation"))

        for sensor in sensors:

            dict[sensor] = dict[sensor].drop(columns=["seconds_elapsed"])

            if sensor == "Accelerometer" or sensor == "Location":
                temp = tsfresh.extract_features(dict[sensor], column_id="ID",
                                                default_fc_parameters=tsfresh.feature_extraction.MinimalFCParameters(),
                                                n_jobs=4)

                if sensor == "Location":  # Orientation Stuff. I don't get it better merged, tbh
                    temp["roll__standard_deviation"] = dict["Orientation"]["roll"].std()
                    temp["roll__variance"] = dict["Orientation"]["roll"].var()
                    temp["roll__root_mean_square"] = rms(dict["Orientation"]["roll"])

                    temp["pitch__standard_deviation"] = dict["Orientation"]["pitch"].std()
                    temp["pitch__variance"] = dict["Orientation"]["pitch"].var()
                    temp["pitch__root_mean_square"] = rms(dict["Orientation"]["pitch"])
                    temp["pitch__absolute_maximum"] = dict["Orientation"]["pitch"].abs().max()

                    temp["yaw__standard_deviation"] = dict["Orientation"]["yaw"].std()
                    temp["yaw__variance"] = dict["Orientation"]["yaw"].var()

                ff_list.append({"data": temp.copy(), "sensor": sensor})


            elif sensor == "Gravity":
                temp["Magnitude(grav)__sum_values"] = dict[sensor]["Magnitude(grav)"].sum()
                temp["Magnitude(grav)__mean"] = dict[sensor]["Magnitude(grav)"].mean()
                temp["Magnitude(grav)__minimum"] = dict[sensor]["Magnitude(grav)"].min()

            elif sensor == "Orientation":
                continue

    return ff_list

def combine(final_form_data_list):
    very_final_form_data_list = []

    for sensor in sensors:
        if sensor == "Orientation":
            continue
        temp_list = []
        for dict in final_form_data_list:
            if str(dict["sensor"]) == str(sensor):
                temp_list.append(dict["data"])
        concat_temp = pd.concat(temp_list)
        very_final_form_data_list.append(concat_temp)


    #Join all the Dataframes to one Dataframe
    df_final = pd.concat(very_final_form_data_list, axis = 1)

    #Drop duplicate "activity" Columns
    #d = df_final.T.drop_duplicates().T
    #df_final = df_final.drop(columns=["activity"])

    #df_final["activity"] = d["activity"]

    #Final Dataframe with all the transformed data
    return df_final


class activityCountMapper:
    activity: str
    count: int

    def __init__(self, act: str):  # Konstruktor der Klasse
        self.activity = act
        self.count = 1

    def countUp(self):
        self.count += 1

    def getActivity(self) -> str:
        return self.activity

    def getCount(self) -> int:
        return self.count

def create_time_line_data(dataList:list):
    returnList = []
    global latestElement
    latestElement = None

    for entry in dataList:
        if latestElement == None:
            latestElement = str(entry)
            returnList.append(activityCountMapper(str(entry)))
            #st.write("Start:" + latestElement)
        elif str(entry) == latestElement:
            returnList[len(returnList) -1].countUp()
            #st.write(latestElement + " wird um 1 erhöht")
        elif str(entry) != latestElement:
            returnList.append(activityCountMapper(str(entry)))
            latestElement = str(entry)
            #st.write("Neue Aktivität " + )

    return returnList

def time_line_data_to_tupel(time_line):
    tupel_list = []
    for entry in time_line:
        tupel_list.append((entry.getActivity(),entry.getCount()))

    return tupel_list

### Pythonic Area

### Streamlit Area

st.subheader("Lets classify your mobility!")
st.write("First we need some Input from you")
#uploaded_file = st.file_uploader("Please upload a sensor data file. JSON or .zip containing CSVs are allowed")
#knn = torch.load(r"..\Models" + "\\" + "KNN (hpo)_2023-06-02")
def main():
    uploaded_file = st.file_uploader("Please upload a sensor data file. JSON or .zip containing CSVs are allowed", accept_multiple_files=False)
    if st.button("Classify me!"):
        prediction_data, gps, metric_data, raw_predictions = process_data(uploaded_file)
        st.header("prediction_data")
        st.write(prediction_data)
        st.header("gps")
        st.write(gps)
        st.header("metric_data")
        st.write(metric_data)
        st.header("raw_predictions")
        st.write(raw_predictions)
        st.subheader("Der Ursprung deiner Daten")
        st.write("Keine Sorge, nur du kannst diese Daten sehen, wir haben nicht genug Geld für Streamlit Pro, daher können wir die nicht speichern ;D")
        st.map(gps)
        st.subheader("Dein Fortbewegungsgraph")
        output_string = ""
        import graphviz
        graph = graphviz.Digraph()
        i = 0
        if len(prediction_data) > 1:
            while i < len(prediction_data) -1:
                graph.edge((prediction_data[i][0] + " " + str(prediction_data[i][1]) + " min"), (prediction_data[i+1][0] + " " + str(prediction_data[i+1][1]) + " min"))
                i += 1
        else:
            graph.edge(prediction_data[i][0] + " " + str(prediction_data[i][1]) + " min", "End")
        st.write(output_string)
        st.graphviz_chart(graph)

        st.subheader("Deine Fortbewegungsverteilung")
          ###############################################################################################
            ###############################################################################################
              ###############################################################################################
                ###############################################################################################
        ###############################################################################################
        ### Zeitstrahl
        # Extrahieren der Aktivitäten und Häufigkeiten aus dem JSON
        aktivitaeten = [key[0] for key in prediction_data]
        haeufigkeiten = [key[1] for key in prediction_data]

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

        ### Balkendiagramm
        activities = {
            "car": 0,
            "bike": 0,
            "walk": 0,
            "subway": 0,
            "idle": 0,
            "roller": 0
        }
        for entry in raw_predictions:
            dict[entry] += 1

        # Erstellen eines DataFrames aus dem Wörterbuch
        df = pd.DataFrame.from_dict(activities, orient='index', columns=['value'])
        bar = px.bar(
            df,
            x='value',
            orientation='v',
            title='Aktivitäten',
            color='value',
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

        ### Kalorienzähler
        def berechne_kalorien_bike(json_data, aktivitaet):
            kalorien_verbrauch = 0
            for item in json_data:
                if item[0] == aktivitaet:
                    minuten = item[1]
                    kalorien_verbrauch += minuten * 6
            return kalorien_verbrauch

        def berechne_kalorien_walk(json_data, aktivitaet):
            kalorien_verbrauch = 0
            for item in json_data:
                if item[0] == aktivitaet:
                    minuten = item[1]
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
          ###############################################################################################
            ###############################################################################################
              ###############################################################################################
                ###############################################################################################
        ###############################################################################################      
            ###############################################################################################
              ###############################################################################################
                ###############################################################################################
        ###############################################################################################
if __name__ == "__main__":
    main()



