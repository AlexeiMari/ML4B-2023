import requests
import json
import streamlit as st 
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Mobility Classification App", page_icon=":oncoming_automobile:", layout="wide")

st.header("Wie kamen wir auf diese Idee?")
st.write("Das Leben als Student ist eine anspruchsvolle Herausforderung. Neben den Vergnügungen wie Feiern, Schlafen und das Genießen des Lebens, müssen wir uns zusätzlich mit den akademischen Pflichten auseinandersetzen. Doch unsere Universität und insbesondere unser Lehrstuhl haben beschlossen, dass es nicht ausreichend schwierig ist. Deshalb werden die bedauernswerten Wirtschaftsinformatikstudenten zusätzlich zu all dem bereits Genannten auch noch gezwungen, in eine andere Stadt zu pendeln.")
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
party, student = st.columns(2)
with party:
    lottie_party = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_6aYlBl.json")
    st_lottie(lottie_party, width=800, height=600)
with student:
    lottie_student = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_dxscbaot.json")
    st_lottie(lottie_student, width=800, height=600)

st.subheader("Deswegen kam uns eine geniale Idee!")
st.write("Du kannst tatsächlich deinen Weg von zuhause bis zur Uni verfolgen, indem du die Sensordaten deines Smartphones nutzt. Das Ding zeichnet quasi auf, wie du dich fortbewegst - ob du läufst, radelst oder dich wie ein gestrandeter Wal auf öffentliche Verkehrsmittel wirfst. Du kannst dann genau sehen, welches Verkehrsmittel du genommen hast und wie viel Zeit du dafür brauchst. Echt praktisch, um herauszufinden, ob du besser den Bus nimmst oder doch evtl. das Auto.")
st.header("Hier kommt die Karte hin")

st.subheader("Was ist noch möglich?")
st.write("Aber das ist noch längst nicht alles! Hier kommt der Clou: Stell dir vor, du bist ein echter Berufspendler und zeichnest deine tägliche Strecke auf. Dann kannst du zu deinem Boss marschieren und ihm die Daten präsentieren. Wer weiß, vielleicht handelst du dir ein schickes Geschäftsauto ein oder verlangst, dass deine Kosten für öffentliche Verkehrsmittel vom Unternehmen übernommen werden. Das ist doch mal eine geniale Möglichkeit, deine Pendelei in bare Münze umzuwandeln!")
lottie_travel = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_MD3DJlKeqe.json")
st_lottie(lottie_travel)