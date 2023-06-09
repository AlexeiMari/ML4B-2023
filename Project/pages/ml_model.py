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
###
st.header("Thank you for the answers!")
with st.container():
    st.write("---")
    st.subheader("Now lets see, if you said the truth!")
    st.write("Now submit your data and our model will predict your mobility type. No worries, you can import json or csv files!")
    uploaded_file = st.file_uploader(label=" ", accept_multiple_files=False)
    st.write("---")


