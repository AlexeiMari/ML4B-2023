import streamlit as st
### Eventuell noch mehr Fragen, falls das zu wenig ist
# Frage zu Flexibilität
# Frage zu Komfort
####

# Frage zu Umwelt
# Frage zu Gesundheit
# Frage zu Sicherheit(Jokes on you, you can always die)
# Frage zu Kosten
# Frage zu Zeit
###Page Config
st.set_page_config(page_title="Mobility Classification App", layout="wide", page_icon=":oncoming_automobile:", initial_sidebar_state="collapsed")
bg_enviroment = '''
<style>
[data-testid="stAppViewContainer"] {
background-image: url("https://s4z3h6y3.rocketcdn.me/wp-content/uploads/2020/10/human-environment-interaction.jpg");
background-size: cover;
}
</style>
'''
st.markdown(bg_enviroment, unsafe_allow_html=True)

###

with open('style.css') as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


st.header("Lets start with the first question!")
st.text("Do you care about the Enviroment?")

anwser_first = ""
answer = st.radio(
    " ",
    ('Yes', 'No', 'Who cares?'))

if answer == 'Yes':
    anwser_first = 1
elif answer == 'No':
    anwser_first = 2
elif answer == 'Who cares?':
    anwser_first = 3

col1, col2, col3 , col4, col5, col6, col7 = st.columns(7)

with col1:
    pass
with col2:
    pass
with col3:
    pass
with col4:
    pass
with col5 :
    pass
with col6 :
    st.markdown('<a href="/second_question" target="_self"><button>Next</button></a>', unsafe_allow_html=True)
with col7 :
    pass


