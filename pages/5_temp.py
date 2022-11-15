import streamlit as st
from utils.data_loader import DataHolder
from utils.models import Modelprovider
import pandas as pd

if 'dh' not in st.session_state:
    st.session_state['dh'] = DataHolder()

if 'mp' not in st.session_state:
    st.session_state['mp'] = Modelprovider()

def update_list():
    res = st.session_state['dh'].get_data_by_orcid(st.session_state['text_in'])
    kwords = []
    for elem in res:
        kwords.extend(st.session_state['mp'].extract_kw(elem[0]))
    st.dataframe(pd.DataFrame(kwords,columns=['Kword','Score']).sort_values("Score",ascending=False),use_container_width=True)

st.text_input("ORCID",key='text_in',on_change=update_list)