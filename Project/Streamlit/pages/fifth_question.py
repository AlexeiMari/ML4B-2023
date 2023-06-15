import streamlit as st
###Page config
st.set_page_config(page_title="Mobility Classification App", layout="wide", page_icon=":oncoming_automobile:", initial_sidebar_state="collapsed")
bg_time = '''
<style>
[data-testid="stAppViewContainer"] {
background-image: url("https://images.unsplash.com/photo-1501139083538-0139583c060f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dGltZXxlbnwwfHwwfHx8MA%3D%3D&w=1000&q=80");
background-size: cover;

}
</style>
'''

st.markdown(bg_time, unsafe_allow_html=True)
###

with open('style.css') as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)



st.header("Last Question!")
st.text("How important is \"Time\" for you?")

anwser_fifth = ""
answer = st.radio(
    " ",
    ('Very important', 'Not important at all', 'I´m not important enough to care about time'))

if answer == 'Very important':
    anwser_fifth = 1
elif answer == 'Not important at all':
    anwser_fifth = 2
elif answer == 'I´m not important enough to care about time':
    anwser_fifth = 3

col1, col2, col3 , col4, col5, col6, col7 = st.columns(7)

with col1:
    pass
with col2:
        st.markdown('<a href="/fourth_question" target="_self"><button>Previous</button></a>', unsafe_allow_html=True)
with col3:
    pass
with col4:
    pass
with col5 :
    pass
with col6 :
    st.markdown('<a href="/ml_model" target="_self"><button>Finish</button></a>', unsafe_allow_html=True)
with col7 :
    pass
