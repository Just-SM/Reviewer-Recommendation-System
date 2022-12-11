import streamlit as st 
from .common_utils import move_next_page

from subprocess import Popen, PIPE
import sys
import json
import utils.utils as utl


def source2_get_data_from_database():
    st.session_state['ar_persons'] = []

    commands = []

    for orcid in st.session_state['ar_orcid_ids']:
        commands.append(str(sys.executable) +
                        r" sources_and_filters\database_data_script.py " + str(orcid))

    with st.spinner("Loading data from DataBase"):
        procs = [Popen(i, text=True, stdout=PIPE) for i in commands]
        for p in procs:
            p.wait()
        for p in procs:
            data_person_raw = json.loads(p.communicate()[0])
            kwords_form_title = None
            if data_person_raw['4'] is not None:
                kwords_form_title = []
                for title in data_person_raw['4']:
                    kwords_form_title.extend(
                        [x[0]for x in st.session_state['mp'].extract_kw(title[0])])
                kwords_form_title = list(set(kwords_form_title))
                for kw in kwords_form_title:
                    if kw in st.session_state['mp'].kwords:
                        st.session_state['mp'].kwords[kw] += 1
                    else:
                        st.session_state['mp'].kwords[kw] = 1
            st.session_state['ar_persons'].append(utl.PersonData(
                data_person_raw['1'], data_person_raw['0'], data_person_raw['3'], kwords_form_title, data_person_raw['2']))

    move_next_page()