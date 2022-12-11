import streamlit as st 
from .common_utils import move_next_page


if 'work_flow_stage' not in st.session_state:
    print ("'work_flow_stage' = 0 set in s1")
    st.session_state['work_flow_stage'] = 0

def file_uploaded():
    df_rev = st.session_state['ar_reviewers_file'].getvalue().decode("utf-8")
    st.session_state['ar_orcid_ids'] = [x.strip() for x in df_rev.split("\n")]
    move_next_page()

def source1_get_reviewers():
    st.markdown("# Load file with Reviewers")
    st.file_uploader("Reviewers File ", ['.txt'], key='ar_reviewers_file', on_change=file_uploaded)