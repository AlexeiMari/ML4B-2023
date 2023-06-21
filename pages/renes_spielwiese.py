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
         "ein Datenpunkt in unserem Datenbestand. In unserem Datenbestand, mit dem wir das Modell trainiert haben, haben wir pro Kategorie ungefähr 300 Datenpunkte."
         "Das macht 5h an Daten pro Kategorie. Im Endeffekt haben wir noch mehr Daten, da manche Fortbewegungsarten leichter unzusetzen waren als andere im großen Stil"
         ", aber runden wir das einfach Mal auf 300 ab. Also haben wir abgerundet 30h an Daten für dieses Projekt gesammelt.")
st.write("Die Daten, die wir verwenden sind Sensordaten, die wir mit 6 verschiedenen Handys aufgenommen haben. "
         "Die Sensordaten konnten wir mit der Sensorlogger App sammeln und exportieren, so dass wir damit arbeiten konnten.")
st.write("")
st.write("Und ja, keine Bewegung war mit Abstand am leichtesten zu sammeln und U-Bahn mit Abstand am anstrengendsten. Wir können niemandem eine 5h U-Bahn Fahrt empfehlen...")

st.header("Der Weg von den Rohdaten zum Machine Learning Modell")
st.subheader("Datenverarbeitungspipeline")
