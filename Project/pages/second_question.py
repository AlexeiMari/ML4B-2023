import streamlit as st
###Page config
st.set_page_config(page_title="Mobility Classification App", layout="wide", page_icon=":oncoming_automobile:", initial_sidebar_state="collapsed")
bg_health = '''
<style>
[data-testid="stAppViewContainer"] {
background-image: url("https://www.lebensmittelverband.de/fileadmin/Seiten/Lebensmittel/Werbung/Claims/AdobeStock_220793275_udra11_1920x1005px.jpg");
background-size: cover;

}
</style>
'''

st.markdown(bg_health, unsafe_allow_html=True)
###

with open('style.css') as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)



st.header("Second question!")
st.text("Do you care about your Health?")
anwser_second = ""
answer = st.radio(
    " ",
    ('Yes', 'No', 'You are kidding?'))

if answer == 'Yes':
    anwser_second = 1
elif answer == 'No':
    anwser_second = 2
elif answer == 'You are kidding?':
    anwser_second = 3

col1, col2, col3 , col4, col5, col6, col7 = st.columns(7)

with col1:
    pass
with col2:
        st.markdown('<a href="/first_question" target="_self"><button>Previous</button></a>', unsafe_allow_html=True)
with col3:
    pass
with col4:
    pass
with col5 :
    pass
with col6 :
    st.markdown('<a href="/third_question" target="_self"><button>Next</button></a>', unsafe_allow_html=True)
with col7 :
    pass
