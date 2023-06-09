import streamlit as st
###Page config
st.set_page_config(page_title="Mobility Classification App",layout="wide", page_icon=":oncoming_automobile:", initial_sidebar_state="collapsed")
bg_safety = '''
<style>
[data-testid="stAppViewContainer"] {
background-image: url("https://isqua.org/media/k2/items/cache/cf4507ae4969876df39b5f798b6f40ce_XL.jpg");
background-size: cover;

}
</style>
'''

st.markdown(bg_safety, unsafe_allow_html=True)
###

with open('style.css') as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)



st.header("Third question!")
st.text("Do you care about your Safety?")

anwser_third = ""
answer = st.radio(
    " ",
    ('Yes', 'No', 'Who cares about safety?'))

if answer == 'Yes':
    anwser_third = 1
elif answer == 'No':
    anwser_third = 2
elif answer == 'Who cares about safety?':
    anwser_third = 3



col1, col2, col3 , col4, col5, col6, col7 = st.columns(7)

with col1:
    pass
with col2:
        st.markdown('<a href="/second_question" target="_self"><button>Previous</button></a>', unsafe_allow_html=True)
with col3:
    pass
with col4:
    pass
with col5 :
    pass
with col6 :
    st.markdown('<a href="/fourth_question" target="_self"><button>Next</button></a>', unsafe_allow_html=True)
with col7 :
    pass
