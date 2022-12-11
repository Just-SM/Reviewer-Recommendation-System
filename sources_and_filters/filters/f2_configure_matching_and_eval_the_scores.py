import streamlit as st 

from ..common_utils import move_next_page


def update_max_persons():
    st.session_state['max_papers_per_person'] = (st.session_state['min_persons_per_doc'] * len(st.session_state['ar_submission_pd'])) // len(st.session_state['ar_persons']) +1


def evaluate_candidates(norm_factor = 0):
    st.session_state['mp'].prep_papers(st.session_state['ar_submission_pd'])
    st.session_state['mp'].prep_persons(st.session_state['ar_persons'],norm_factor)


def filter2_configure_matching_and_eval_the_scores():

    if  'number_of_candidates_per_paper' not in st.session_state:
        st.session_state['number_of_candidates_per_paper'] = []
    if 'ar_dict_of_number_assignments' not in st.session_state:
        st.session_state['ar_dict_of_number_assignments'] = dict()

    st.markdown("### Start Evaluation")
    st.write("🔨 Some configurations should be here")
    if 'max_papers_per_person' not in st.session_state:
        st.session_state['max_papers_per_person'] = len(st.session_state['ar_submission_pd'])//len(st.session_state['ar_persons']) + 1
    st.session_state['save_max_papers_per_person'] =  st.number_input("Number of maximum papers for each person",1, len(st.session_state['ar_submission_pd']),key='max_papers_per_person')
    st.number_input("Default number of candidates per page displayed",1, 10,4,key='default_number_of_candidates')
    st.session_state['save_max_candidates_per_paper'] = st.number_input("Max number of persons per doc", 1, len(st.session_state['ar_persons']),1,key='ar_max_candidates_per_paper')
    st.session_state['save_min_persons_per_doc'] = st.number_input("Min number of persons per doc",1,len(st.session_state['ar_persons']),1,key='min_persons_per_doc')
    # st.checkbox("Priority is affected by number of assigned papers",value=False)
    st.checkbox("Normalize number of keywords",value=True,key="normalize_keywords",help="Normalize the value of the vectors to avoid the over-grade by amount of vectors")
    if st.session_state['normalize_keywords']:
        st.slider("Normalization factor",0.0,1.0,0.6,key='norm_factor',help="Meaning is every subsequent keyword will be weighted by a factor less")
    else:
        st.session_state['norm_factor'] = 0
    # st.selectbox("Auto-fill method",["Best matches for paper","Best matches for person","Reviewer - Paper best matches"])
    
    if st.session_state['min_persons_per_doc'] * len(st.session_state['ar_submission_pd']) <= st.session_state['save_max_papers_per_person'] * len(st.session_state['ar_persons']):
        if st.button("Start"):
            with st.spinner("Loading the model"):
                st.session_state['mp'].load_vectorizer()
            with st.spinner("Loading the papers"):
                evaluate_candidates(st.session_state['norm_factor']/25)
            with st.spinner("Evaluating the candidates"):
                st.session_state['result'] = []
                for ind, paper in st.session_state['ar_submission_pd'].iterrows():

                    st.session_state['number_of_candidates_per_paper'].append(st.session_state['default_number_of_candidates'])
                    found_persons = st.session_state['mp'].find_matches_for_paper(paper = paper,top_n=st.session_state['default_number_of_candidates'])
                    
                    st.session_state['result'].append((ind, paper['title'], paper['keywords'], paper['abstract'],paper['authors'], found_persons))
                    for person,score in found_persons:
                        if person.orcid not in st.session_state['ar_dict_of_number_assignments']:
                            st.session_state['ar_dict_of_number_assignments'][person.orcid] = 0

            move_next_page()
            st.session_state['sidebar_state'] = 'collapsed'
            st.experimental_rerun()
    else:
        st.markdown("The number of papers is greater than reviewers can hold ❗")
        st.button("Adjust number of papers per person ?",on_click=update_max_persons)
        st.button("Start",key="start_button_other_key",disabled=True)
