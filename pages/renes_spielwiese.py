import streamlit as st

st.title("How it works")
st.write("Die Technik hinter unserer Seite")

st.header("Die Basics")
st.write("Unsere Seite verwendet ein Machine Learning Modell, welches darauf trainiert wurde, Fortbewegungsarten zu klassifizieren. Unser Modell kann bisher zwischen"
         "sechs verschiedenen Klassen unterscheiden. Diese sind")
st.markdown("- Auto")
st.markdown("- Motorroller")
st.markdown("- Fahrrad")
st.markdown("- Laufen")
st.markdown("- U-Bahn")
st.markdown("- Keine Bewegung")
st.markdown('''
<style>
[data-testid="stMarkdownContainer"] ul{
    padding-left:40px;
}
</style>
''', unsafe_allow_html=True)

st.write("Wir hätten sogar fast Flugzeuge noch mit reingenommen, aber der Flugzeugmodus hat die Daten manipuliert, daher müssen diese sechs erstmal reichen")

st.header("Die Daten")
st.write("Wie viele Daten braucht man, um eine Glühbirne zu wechseln?")
st.write("Keine Ahnung, aber zum trainieren von einem Machine Learning Modell braucht man eine Menge.")
st.write("Unser Modell ist darauf trainiert worden, einminütige Sequences zu klassifizieren, demnach ist jede Sequenz, die eine Minute lang geht, "
         "ein Datenpunkt in unserem Datenbestand. In unserem Datenbestand, mit dem wir das Modell trainiert haben, haben wir pro Kategorie ungefähr 350 Datenpunkte."
         "Das macht 5h an Daten pro Kategorie. Im Endeffekt haben wir noch mehr Daten, da manche Fortbewegungsarten leichter unzusetzen waren als andere im großen Stil"
         ", aber runden wir das einfach Mal auf 350 ab. Also haben wir abgerundet 35h an Daten für dieses Projekt gesammelt.")
st.write("Die Daten, die wir verwenden sind Sensordaten, die wir mit 6 verschiedenen Handys aufgenommen haben. "
         "Die Sensordaten konnten wir mit der Sensorlogger App sammeln und exportieren, so dass wir damit arbeiten konnten.")
st.write("")
st.write("Und ja, keine Bewegung war mit Abstand am leichtesten zu sammeln und U-Bahn mit Abstand am anstrengendsten. Wir können niemandem eine 5h U-Bahn Fahrt empfehlen...")

st.header("Der Weg von den Rohdaten zum Machine Learning Modell")
st.header("Datenverarbeitungspipeline")
st.subheader("Die Daten in der Pipeline")

st.write("Zuerst mussten wir uns überlegen, was für Sensordaten wir genau verwenden möchten, entschieden haben wir uns dann für die Folgenden drei:")

sensors = '''sensors = ["Accelerometer","Location","Orientation"]'''
st.code(sensors, language="python")

st.write("Wir verwalten die Sensoren in einer Liste, da unsere Pipeline dynamisch genug ist, um Sensoren aus dem Prozess zu entfernen und neue hinzuzufügen, solange diese in allen "
         "Datzensätzen auch aufgenommen wurden.")
st.write("")

st.write("Die Sensoren bringen alle mehrere Attribute mit sich, da wir nicht alle von ihnen in ihrer aktuelle vorliegenden Form benötigen, haben wir manche Attribute rausgeworfen und "
         "andere zu neuen Attributen umgeformt. Das ist unser erster Feature-Engineering und Feature Selection Schritt in der Pipeline")
loc_code ='''        if(sensor == "Location"):
            df = df.drop(columns= df.columns.difference(["speed", "Readable_Time", "seconds_elapsed"]))'''
st.code(loc_code, language="python")

acc_code = '''        elif sensor == "Accelerometer":
            df["Magnitude(acc)"] = np.sqrt(df["x"]**2 + df["y"]**2 + df["z"]**2)
            df = df.drop(columns= df.columns.difference(["Magnitude(acc)", "Readable_Time", "seconds_elapsed"]))'''
st.code(acc_code, language="python")

ori_code = '''        elif sensor == "Orientation":
            df = df.drop(columns= df.columns.difference(["roll", "pitch", "yaw","Readable_Time", "seconds_elapsed"]))'''
st.code(ori_code, language="python")

st.write("")
st.write("Wir haben auch versucht, den Gravity Sensor mit reinzunehmen, aber bei der Feature-Importance Analyse hat sich herausgestellt, dass der Sensor kaum Auswirkungen hat,"
         " aber zu der Feature-Importance Analyse und später mehr")

st.write("")

st.subheader("Der Pipelineprozess")
st.write("Ok, jetzt, wo wir wissen, welche Sensordaten wir genau benutzen, müssen wir darüber reden, was wir eigentlich genau machen wollen.")
st.write("Der Plan ist, die Zeitreihen zu normalisieren und als Vektoren von Metriken zu speichern. Die Tabellen, die die Sensordaten speichern, sind die Zeitreihe einer Aufnahme in"
         "Tabellenform. Wir nehmen daher die Zeitreihen, also unsere Aufnahmen, schneiden sie in gleichlange Teile und berechnen dann über diese Teile Metainformationen, "
         "oder auch Metriken / Kennzahlen. Ein Beispiel für so eine Metrik wäre die durchschnittliche Geschwindigkeit (speed). Damit können wir aus einer Tabelle einen Tabelleneintrag machen."
         "Jede Zeitreihe wird also zu einer Reihe in dem Trainingsdatensatz, mit dem wir unser ML Modell trainieren möchten")