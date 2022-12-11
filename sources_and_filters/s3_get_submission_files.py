import streamlit as st 

import pandas as pd

from .common_utils import move_next_page

def update_submission_file():
    st.session_state['ar_submission_pd'] = pd.read_csv(
        st.session_state['ar_submission_file_raw'], index_col=['#'])
    st.session_state['ar_submission_pd'] = st.session_state['ar_submission_pd'][[
        "title", 'keywords', 'abstract','authors']]
    move_next_page()

def source3_get_submission_files():
    st.markdown("Upload a submission file")
    st.file_uploader('Submission', ['.csv'], key="ar_submission_file_raw", on_change=update_submission_file)
