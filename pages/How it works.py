import streamlit as st
st.set_page_config(page_title="Mobility Classification App", page_icon=":oncoming_automobile:", layout="wide", initial_sidebar_state="collapsed")
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
st.markdown("- Bewegungslos")
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
st.write("Der Plan ist, die **Zeitreihen zu normalisieren** und als **Vektoren von Metriken** zu speichern. Die Tabellen, die die Sensordaten speichern, sind die Zeitreihe einer Aufnahme in"
         " Tabellenform. Wir nehmen daher die Zeitreihen, also unsere Aufnahmen, schneiden sie in gleichlange Teile und berechnen dann über diese Teile Metainformationen, "
         "oder auch Metriken / Kennzahlen. Ein Beispiel für so eine Metrik wäre die durchschnittliche Geschwindigkeit (speed). **Damit können wir aus einer Tabelle einen Tabelleneintrag machen**. "
         "Jede Zeitreihe wird also zu einer Reihe in dem Trainingsdatensatz, mit dem wir unser ML Modell trainieren möchten")
st.image("Pipeline Prozess.png", caption = "Der Pipelineprozess abstrahiert")
st.write("")
st.image("Zeitreihennormalisierung.png", caption = "Normalisierung der Zeitreihendaten abstrahiert")
st.write("")

st.subheader("Die Daten - Erneut")
st.write("Der erste Schritt des Pipelineprozesses ist, die aufgenommen Daten in das Python Projekt einzulesen. Da begegnen wir bereits dem ersten Problem, das Dateiformat. Die Sensorlogger App, "
         "die wir verwendet haben, ermöglicht es uns, die Daten in zwei Formaten zu exportieren, als **JSON** oder als **CSV**.")
st.write("Exportiert man die Daten als CSV, erhält man eine ZIP, in der für jeden aufgenommenen Sensor eine CSV Datei liegt.")
st.write("Exportiert man die Daten als JSON erhält man eine einzelne JSON, diese enthält alle Daten über alle Sensoren.")
st.write("Das Ganze ist ein Problem, weil die Daten in einer anderen Form vorliegen, je nachdem, über welches Format sie exportiert und dann in das Projekt eingelesen wurden. "
         "Liest man mit Pandas eine JSON ein, bekommt man einen einzelnen Dataframe mit allen Attributen von allen Sensoren. Die Sensoren sind aber nicht aufeinander gejoint worden, das heißt, "
         "wenn ich eine 10 Minuten Aufnahme hätte und jede Minute einmal die Sensordaten erfassen würde, hätte ich einen Dataframe mit x * 10 Einträgen, wobei x die Anzahl an Sensoren ist. "
         "Die Attribute, die ein Sensor nicht aufnimmt, sind dann None.")
st.write("Der CSV Export stellt uns eine CSV für jeden Sensor zur Verfügung. Also müssen wir hier für jeden Sensor einen Dataframe anlegen.")
st.write("Diese beiden Dataframe Formate sind nicht miteinander kompatibel und unterscheiden sich zu stark voneinander, als dass man ohne eine Formatsangleichung weiter machen könne. "
         "Hier haben wir nun drei Möglichkeiten, wir passen die JSON and die CSV an, wir passen die CSV an die JSON an oder wir lassen nur ein Dateiformat zu.")
st.write("Die dritte Option ist für unseren Fall keine Option gewesen, da die Sensorlogger App Aufnahmen, die eine gewissen Dateigröße überschreiten, nicht mehr als JSON, sonder nur noch als"
         " CSV exportieren kann. Wir hätten also JSONs einfach kicken können, aber das wäre einfach unschön gewesen.")
st.write("Wir haben uns am Ende dazu entschieden, die JSON an die CSV anzupassen.")

st.image("Datenanpassung.png", caption = "Datenanpassung mit den transform_data Methoden")

st.write("Die Grafik zeigt, wie wir unsere Daten anpassen. Aus jeder JSON und jeder ZIP, die CSVs enthält, werden Dictionaries, die jeden Sensornamen einen Dataframe zuordnen. Zusätzlich dazu haben "
         "alle Dicts auch noch einen Key namens label. label speichert die Aktivität, die während dieser Aufnahme durchgeführt wird. Am Ende sind all unsere JSONs und CSVs als "
         "Dictionaries in einer Liste. Das ist unser transformierter Datenbestand.")
st.write("")
st.write("")
st.write("Die Daten sind nun einheitlich eingelesen, jetzt haben wir noch das Problem, dass die Aufnahmen der Sensordaten nicht (immer) gleich lang sind. Das Problem lässt sich aber leicht lösen.")
st.write("Jede Aufnahme von hat ein Attribut namens seconds_elapsed. Wie der Name vermuten lässt, gibt es an, wie viele Sekunden zu jedem Datenpunkt einer Aufnahme vergangen sind. Um herauszufinden,"
         "wie lange eine Aufnahme geht, müssen wir nur den letzten Datenpunkt einer Aufnahme anschauen un dessen seconds_elapsed auslesen.")
st.write("Um die Aufnahmen in die gleiche Länge zu bekommen, haben wir die Methode split_data() geschrieben. Sie nimmt ein Dictionary und und gibt eine Liste von Dictionaries zurück, "
         "die alle die gleiche Länge haben, die man angibt. Im Beispiel der folgenden Abbildung wird ein Dictionary, das eine 10 Minuten Aufnahme repräsentiert, in 10 Dictionaries aufgeteilt, die jeweils"
         "eine Minute lang sind.")

st.image("Split.png", caption = "Datenaufteilung mit den split_data Methode")
st.write("")

st.subheader("Metriktransformation")
st.write("Die ersten beiden Schritte von unserem abstrakten Transformationsprozess sind nun abgeschlossen, wir haben die Daten einheitlich eingelesen und in gleiche Stücke aufgeteilt.")

st.write("Nun müssen wir noch die Metriken über die aufgeteilten Stücke berechnen. Dieser Schritt war... ein Problem. Hierfür haben wir die Methode calculate_features() implementiert. "
         "Diese Methode nimmt ein Dictionary und gibt eine Liste zurück. Diese Liste enthält für jeden Sensor, der verwendet wurde, ein Dictionary. Dieses neue Dictionary weist dem Key 'data' "
         "einen Dataframe zu, der genau eine Reihe hat. Die Spalten des Dataframes sind die verwendeten Metriken, die Reihe speichert die Werte. Dem Key 'sensor' weist es einen String zu. Hier "
         "also, zu welchem Sensor diese Metriken gehören.")

st.image("CalculateFeatures.png", caption = "Metrikberechnung mit der calculate_features Methode")

st.write("")
st.write("Jetzt ist natürlich interessant, wie wir unsere Metriken genau berechnen und warum dieser Schritt ein Problem war, denn die Implementierung war es nicht :D.")
st.write("Für die Berechnung der Metriken bzw Features verwenden wir die Library tsfresh. tsfresh ist eine Library, die aus Zeitreihen  Metriken berechnen kann und auch Metriken-Pakete "
         "mitbringt, die man benutzen kann. tsfresh berechnet für jedes Attribut 10 Metriken, wenn man die wenigsten Features einstellt (was wir getan haben). Da wir über alle Sensoren "
         "hinweg 5 Attribute haben, berechnet tsfresh 50 Metriken. Als wir noch mehr als 5 Attrtibute verwendet haben, hatten wir über 90 Features.")
st.write("Und jetzt kommen wir zum Problem, das hat richtig schlecht performt. Unseren ganzen Datenbestand zu transformieren hat >6h gebraucht. Das war noch nicht Mal das größte Problem, "
         "auf unserer ersten Version der Streamlit Seite hat dieser ganze Prozess für wenige Daten sehr sehr lange gebraucht. Ohne daran was zu ändern, wäre die Seite schlicht nicht nutzbar.")
st.write("Spoiler, wir haben das Problem gelöst, aber wie? Den ersten Lösungsschritt haben wir weiter oben schon gesehen, wir haben Attribute zusammengefasst oder ganz rausgenommen. "
         "Aus den drei Attributen, die der Accelerometer liefert, haben wir ein neues gebildet und vom Orientation Sensor haben wir alle Features bis auf drei rausgeworfen.")
st.write("Welche Attribute wir rauswerfen haben wir anhand der Feature Importance eines Random Forests, den wir mit den Daten trainiert haben, entschieden.")
st.write("Das hat die Performance verbessert, aber gut war sie immer noch nicht. Als nächstes haben wir uns die Feature Importances von einem Random Forest, der mit den neuen Daten "
         "trainiert wurde, angeschaut.")

st.image("FI.png", caption = "Feature Importances")

st.write("Was wir hier sofort erkennen ist, dass magnitude(acc) und speed Features fast alle eine ziemlich hohe Feature Importance haben, roll, pitch und yaw haben jeweils nur wenige Features, "
         "die wirklich relevant sind. In dieser Abbildung ist der Gravity Sensor auch noch mit drinnen, den haben wir rausgekickt, da er nur ein gutes Feature hervorbringt und weil nicht "
         "alle Aufnahmen, die wir haben, den Gravity Sensor aufgenommen haben.")
st.write("Die Konsequenz, die wir daraus gezogen haben, war, unsere Features auf die wichtigesten zu reduzieren. die Magnitude(acc) und speed Features behalten wir, denn die sind fast alle "
         "sehr wichtig für unser Machine Learning Modell. Die roll, pitch und yaw Features können wir nicht mehr über tsfresh berechnen, da uns nur wenige Features von diesen Attributen interessieren."
         " Also berechnen wir diese paar Features jetzt manuell, für die anderen verwenden wir weiterhin tsfresh")

feature_code = ''' if sensor == "Accelerometer" or sensor == "Location":
                temp = tsfresh.extract_features(dict[sensor], column_id = "ID",
                        default_fc_parameters=tsfresh.feature_extraction.MinimalFCParameters(),
                         n_jobs = 4)'''
st.code(feature_code, language="python")

f2 = '''            
    def rms(df):
        square = df**2
        square = square.sum()
        mean = (square / len(df))
        root = math.sqrt(mean)
        return root
        
                    temp["roll__standard_deviation"] = dict["Orientation"]["roll"].std()
                    temp["roll__variance"] = dict["Orientation"]["roll"].var()
                    temp["roll__root_mean_square"] = rms(dict["Orientation"]["roll"])

                    temp["pitch__standard_deviation"] = dict["Orientation"]["pitch"].std()
                    temp["pitch__variance"] = dict["Orientation"]["pitch"].var()
                    temp["pitch__root_mean_square"] = rms(dict["Orientation"]["pitch"])
                    temp["pitch__absolute_maximum"] = dict["Orientation"]["pitch"].abs().max()

                    temp["yaw__standard_deviation"] = dict["Orientation"]["yaw"].std()
                    temp["yaw__variance"] = dict["Orientation"]["yaw"].var()'''

st.code(f2, language = "python")

st.write("Am Ende der Metrikenberechnung / Feature Calculation bekommt jeder Metrikenvektor noch die Spalte 'label' dazu.")

st.subheader("Zusammenführung")
st.write("Jetzt sind wir im letzen Schritt der Datenvorverarbeitung angekommen. Kurze Zusammenfassung, wir haben jetzt eine Liste mit Dictionaries, die jeweils einen Metrivektor und "
         " einen Sensor speichern. Die einzelnen aufgeteilten Aufnahmen, die zu Metrikverktoren wurden, haben alle eindeutige IDs bekommen, die auch in den Vekotren sind. Über die "
         "kann man die Vektoren wieder zusammenführen.")
st.write("Nun 'brechen' wir die Dictionaries auf. Wir konkatenieren die Metrikvektoren der jeweiligen Sensoren, sodass wir pro Sensor genau einen Dataframe haben. Jeder Dataframe hat so viele "
         "Reihen, wie Einträge in der Liste nach der split_data Methode waren. Diese Dataframes konkatenieren wir nun noch vertikal und unsere Daten sind endlich im fertigen Format.")
st.image("FinalenDatensatzZusammenstellen.png", caption = "Zusammenfügung der Metrikvektoren")
st.write("Jetzt haben wir einen Dataframe, mit dem wir ein Machine Learning Modell trainieren können!")

st.header("Machine Learning")

