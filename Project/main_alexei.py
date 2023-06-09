import pandas as pd
import streamlit as st
import csv
import sklearn
import numpy as np
import json
import torch
import math
import os
import tsfresh
import pickle
import zipfile as zf
import requests
from streamlit_lottie import st_lottie 
import json

### Streamlit Area
### Page config
st.set_page_config(page_title="Mobility Classification App", layout="wide", page_icon=":oncoming_automobile:", initial_sidebar_state="collapsed")
bg_gradient = '''
<style>
[data-testid="stAppViewContainer"] {
background: linear-gradient(#e66465, #9198e5);
}
</style>
'''
st.markdown(bg_gradient, unsafe_allow_html=True)
###

with open('style.css') as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)




### First Page
st.header("Welcome to our Mobility Classification App!")


### Lottie Animation Images
#def load_lottieurl(url: str):
#    r = requests.get(url)
#    if r.status_code != 200:
#        return None
#    return r.json()

#lottie_hello_robot = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_rueemnoo.json")

#st_lottie(
#    lottie_hello_robot,
#)

with st.container():

    st.write("---")
    st.subheader("Before we start, we need some information about you!")
    st.write("We are gonna do a little survey. Click on the button to start!")
    st.markdown('<a href="/first_question" target="_self"><button>Click me!</button></a>', unsafe_allow_html=True)
    st.caption("Based on your given choices we can better provide an appropriate answer!")
    st.write("---")


