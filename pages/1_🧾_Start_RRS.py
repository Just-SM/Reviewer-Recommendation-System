import streamlit as st

from sources_and_filters import (source1_get_reviewers,
                                source2_get_data_from_database,
                                source3_get_submission_files,
                                filter1_verify_persons_data,
                                filter2_configure_matching_and_eval_the_scores,
                                sink,
                                ModelProvider,
                                )

if 'sidebar_state' not in st.session_state:
    st.session_state['sidebar_state'] = 'expanded'

if 'work_flow_stage' not in st.session_state:
    st.session_state['work_flow_stage'] = 0

if 'mp' not in st.session_state:
    st.session_state['mp'] = ModelProvider()

st.set_page_config(
    page_title="Add Reviewers",
    page_icon="🎩",
    layout='wide',
    initial_sidebar_state=st.session_state['sidebar_state'],)


if __name__ == '__main__':

    # WORK FLOW 

    if st.session_state['work_flow_stage'] == 0:

        st.session_state['data_pipe'] = source1_get_reviewers ()


    if st.session_state['work_flow_stage'] == 1:

        source2_get_data_from_database()

    if st.session_state['work_flow_stage'] == 2:

        filter1_verify_persons_data()

    if st.session_state['work_flow_stage'] == 3:
       
       source3_get_submission_files()

    if st.session_state['work_flow_stage'] == 4:

        filter2_configure_matching_and_eval_the_scores()

    if st.session_state['work_flow_stage'] == 5:

        sink()