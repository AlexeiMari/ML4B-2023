import streamlit as st
###Page config
st.set_page_config(page_title="Mobility Classification App", layout="wide", page_icon=":oncoming_automobile:", initial_sidebar_state="collapsed")
bg_money = '''
<style>
[data-testid="stAppViewContainer"] {
background-image: url("https://cloudfront-us-east-2.images.arcpublishing.com/reuters/2DPNRZGUSNO45BHUUTP3MY5KSE.jpg");
background-size: cover;
}
</style>
'''
st.markdown(bg_money, unsafe_allow_html=True)
###

with open('style.css') as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)



st.header("We are almost done!")
st.text("How much do your care about Money?")
anwser_fourth = ""
answer = st.radio(
    " ",
    ('A lot', 'Not really', 'First i need money i can care about'))

if answer == 'A lot':
    anwser_fourth = 1
elif answer == 'Not really':
    anwser_fourth = 2
elif answer == 'First i need money i can care about':
    anwser_fourth = 3

col1, col2, col3 , col4, col5, col6, col7 = st.columns(7)

with col1:
    pass
with col2:
        st.markdown('<a href="/third_question" target="_self"><button>Previous</button></a>', unsafe_allow_html=True)
with col3:
    pass
with col4:
    pass
with col5 :
    pass
with col6 :
    st.markdown('<a href="/fifth_question" target="_self"><button>Next</button></a>', unsafe_allow_html=True)
with col7 :
    pass
