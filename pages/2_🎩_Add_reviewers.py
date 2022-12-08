import streamlit as st
import pandas as pd
import utils.utils as utl
from subprocess import Popen, PIPE
import sys
import json
import textwrap

# side bar state, required to be here 
if 'sidebar_state' not in st.session_state:
    st.session_state['sidebar_state'] = 'expanded'

st.set_page_config(
    page_title="Add Reviewers",
    page_icon="🎩",
    layout='wide',
    initial_sidebar_state=st.session_state['sidebar_state'],)

# CREATE PIPES DATA STATES :


### PIPE 1 ###
if 'ar_orcid_ids' not in st.session_state:
    st.session_state['ar_orcid_ids'] = None



# CREATE STATE VARS
if "ar_page_mode" not in st.session_state:
    st.session_state['work_flow_stage'] = 0
if 'mp' not in st.session_state:
    st.session_state['mp'] = utl.Modelprovider()
if 'ar_number_of_person' not in st.session_state:
    st.session_state['ar_number_of_person'] = 0
if 'ar_number_of_paper' not in st.session_state:
    st.session_state['ar_number_of_paper'] = 0
if 'ar_list_of_assigned'not in st.session_state:
    st.session_state['ar_list_of_assigned'] = []
if 'ar_dict_of_number_assignments' not in st.session_state:
    st.session_state['ar_dict_of_number_assignments'] = dict()
if 'picked_candidates' not in st.session_state:
    st.session_state['picked_candidates'] = []
if 'min_persons_per_doc' not in st.session_state:
    st.session_state['min_persons_per_doc'] = 1
# DEF CONFIG
if 'save_max_candidates_per_paper' not in st.session_state:
    st.session_state['save_max_candidates_per_paper'] = 0
if 'number_of_candidates_per_paper' not in st.session_state:
    st.session_state['number_of_candidates_per_paper'] = []
if 'save_max_papers_per_person' not in st.session_state:
    st.session_state['save_max_papers_per_person'] = 1
# DEF FUNCTIONS

def move_next_page():
    st.session_state['work_flow_stage'] += 1


def evaluate_candidates(norm_factor = 0):
    st.session_state['mp'].prep_papers(st.session_state['ar_submission_pd'])
    st.session_state['mp'].prep_persons(st.session_state['ar_persons'],norm_factor)


# def get_persons_form_orcid(orcid):
#     return st.session_state['dh'].get_user_data_by_orcid(orcid)


def next_person():
    st.session_state['ar_number_of_person'] += 1

def update_max_persons():
    st.session_state['max_papers_per_person'] = (st.session_state['min_persons_per_doc'] * len(st.session_state['ar_submission_pd'])) // len(st.session_state['ar_persons']) +1

def next_person_skip():
    while st.session_state[f"{st.session_state['ar_number_of_person']}-name"].strip() != "" and st.session_state[f"{st.session_state['ar_number_of_person']}-orcid"].strip() != "" and st.session_state[f"{st.session_state['ar_number_of_person']}-affiliation"].strip() != "" and (st.session_state[f"{st.session_state['ar_number_of_person']}-given_kwords"].strip() != "" or st.session_state[f"{st.session_state['ar_number_of_person']}-found_kwords"].strip() != "") and st.session_state['ar_number_of_person']+1 < len(st.session_state['ar_persons']):
        next_person()

# def change_page_to_ass_load():
#     st.session_state['ar_all_loaded'] = False
#     st.session_state['ar_assigning_load'] = True

def file_uploaded():

    df_rev = st.session_state['ar_reviewers_file'].getvalue().decode("utf-8")

    st.session_state['ar_orcid_ids'] = [x.strip() for x in df_rev.split("\n")]


def update_submission_file():
    st.session_state['ar_submission_pd'] = pd.read_csv(
        st.session_state['ar_submission_file_raw'], index_col=['#'])
    st.session_state['ar_submission_pd'] = st.session_state['ar_submission_pd'][[
        "title", 'keywords', 'abstract','authors']]
    move_next_page()

# def confirm_selection():
#     for res in st.session_state['picked_candidates']:
#         st.session_state['ar_list_of_assigned'].append(
#         (res[0], res[1], res[2], res[3],res[4], res[5][3]))
#         if res[5][3][0].orcid in st.session_state['ar_dict_of_number_assignments']:
#             st.session_state['ar_dict_of_number_assignments'][res[5]
#                                                             [3][0].orcid] += 1
#         else:
#             st.session_state['ar_dict_of_number_assignments'][res[5]
#                                                             [0][0].orcid] = 1
        

def render_candidates():

    if len(st.session_state['picked_candidates']) >= st.session_state['save_max_candidates_per_paper']:
        
        for ind,(person,score) in enumerate(st.session_state['result'][st.session_state['ar_number_of_paper']][5]):
           
            # st.markdown(person)
            if person.given_kw != ['']:
                if ',' in person.given_kw[0]:
                    kwords = " ".join(person.given_kw[:5])
                else:
                    kwords = ", ".join(person.given_kw[:5])
            else:
                kwords = ", ".join(person.calc_kw[:5])

            st.markdown(
                        f"🎩 Name: {person.name_surname}  \nPapers : {st.session_state['ar_dict_of_number_assignments'][person.orcid]}  \n 🏫 Affiliation: {person.affiliation}  \n🔑 Keywords: {kwords}  \n🌟 Score: {'{:.3f}'.format(score)}")
            
            if person in [x[5][0] for x in st.session_state['picked_candidates']] or st.session_state['ar_dict_of_number_assignments'][person.orcid] >= st.session_state['save_max_papers_per_person']:
                st.checkbox("Select",key=f'p{ind}',on_change=add_choise,)
                
            else:
                st.checkbox("Select",key=f'p{ind}',on_change=add_choise,disabled=True,)
    else:
        for ind,(person,score) in enumerate(st.session_state['result'][st.session_state['ar_number_of_paper']][5]):

            if person.given_kw != ['']:
                if ',' in person.given_kw[0]:
                    kwords = " ".join(person.given_kw[:5])
                else:
                    kwords = ", ".join(person.given_kw[:5])
            else:
                kwords = ", ".join(person.calc_kw[:5])
            if st.session_state['ar_dict_of_number_assignments'][person.orcid] >= st.session_state['save_max_papers_per_person']:
                st.markdown(
                        f"🎩 Name: {person.name_surname}  \nPapers : {st.session_state['ar_dict_of_number_assignments'][person.orcid]}  \n 🏫 Affiliation: {person.affiliation}  \n🔑 Keywords: {kwords}  \n🌟 Score: {'{:.3f}'.format(score)}")
                st.checkbox("Select",key=f'p{ind}',on_change=add_choise,disabled=True,)
            else:
                st.markdown(
                        f"🎩 Name: {person.name_surname}  \nPapers : {st.session_state['ar_dict_of_number_assignments'][person.orcid]}  \n 🏫 Affiliation: {person.affiliation}  \n🔑 Keywords: {kwords}  \n🌟 Score: {'{:.3f}'.format(score)}")
                st.checkbox("Select",key=f'p{ind}',on_change=add_choise,)

def add_choise():
    st.session_state['picked_candidates'] = []

    index,title,keys,abstract,authors,persons = st.session_state['result'][st.session_state['ar_number_of_paper']]
    for ind,person in enumerate(persons):
        if st.session_state[f'p{ind}']:
            st.session_state['picked_candidates'].append((index,title,keys,abstract,authors,person))
    # st.write(st.session_state['picked_candidates'])


def add_more_candidates():
    # 
    # NOT EFFICIENT AT ALL TODO!
    # 
    cur_paper = st.session_state['ar_number_of_paper']

    st.session_state['number_of_candidates_per_paper'][cur_paper] = st.session_state['number_of_candidates_per_paper'][cur_paper] + 2
    found_persons = st.session_state['mp'].find_matches_for_paper(st.session_state['ar_submission_pd'].iloc[cur_paper].to_dict(),st.session_state['number_of_candidates_per_paper'][cur_paper])
    
    st.session_state['result'][cur_paper] =(st.session_state['result'][cur_paper][0], st.session_state['result'][cur_paper][1], st.session_state['result'][cur_paper][2], st.session_state['result'][cur_paper][3],st.session_state['result'][cur_paper][4], found_persons)

    for person,score in found_persons:
        if person.orcid not in st.session_state['ar_dict_of_number_assignments']:
            st.session_state['ar_dict_of_number_assignments'][person.orcid] = 0

def confirm_list_of_candidates():
    for confirmed in st.session_state['picked_candidates']:
        st.session_state['ar_list_of_assigned'].append(confirmed)
        st.session_state['ar_dict_of_number_assignments'][confirmed[5][0].orcid] = st.session_state['ar_dict_of_number_assignments'][confirmed[5][0].orcid] + 1 

    for x in range (st.session_state['number_of_candidates_per_paper'][st.session_state['ar_number_of_paper']]):
        st.session_state[f'p{x}'] = False

    st.session_state['ar_number_of_paper'] += 1
    st.session_state['picked_candidates'] = []
    


def auto_complete_stupid():

    with st.spinner("Auto - completing"):
        for data in st.session_state['result'][st.session_state['ar_number_of_paper']:]:
            (index,title, keywords, abstract,authors,found_persons) = data
            ind = 0
            pack = []
        # try:
            while len(pack) < st.session_state['min_persons_per_doc']:
                person = found_persons[ind]
                if st.session_state['ar_dict_of_number_assignments'][person[0].orcid] <= st.session_state['save_max_papers_per_person']:
                    pack.append(person)
                    if ind + 1 >= len(found_persons):
                        old_val = len(found_persons)
                        found_persons = st.session_state['mp'].find_matches_for_paper((title, keywords, abstract,),len(found_persons)+3)
                        if len(found_persons) > old_val:
                            break 
                    ind += 1
                else:
                    if ind + 1 >= len(found_persons):
                        old_val = len(found_persons)
                        found_persons = st.session_state['mp'].find_matches_for_paper((title, keywords, abstract,),len(found_persons)+3)
                        if len(found_persons) > old_val:
                            break 
                        ind += 1
                    else:
                        ind += 1
            for p in pack:
                st.session_state['ar_list_of_assigned'].append((index,title,keywords,abstract,authors,p))
                st.session_state['ar_dict_of_number_assignments'][p[0].orcid] = st.session_state['ar_dict_of_number_assignments'][p[0].orcid] + 1 
            # except Exception as e:
            #     st.write(data)
            #     st.write(st.session_state['ar_dict_of_number_assignments'])
            #     st.write(pack)
            #     return
    st.session_state['ar_number_of_paper'] = len(st.session_state['result'])

# RUNNERS CODE

def source1_get_reviewers():
    st.markdown("# Load file with Reviewers")

    st.file_uploader("Reviewers File ", ['.txt'], key='ar_reviewers_file', on_change=file_uploaded)

    move_next_page()


def source2_get_data_from_database():
    st.session_state['ar_persons'] = []

    commands = []

    for orcid in st.session_state['ar_orcid_ids']:
        commands.append(str(sys.executable) +
                        r" utils\utils.py " + str(orcid))

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


def filter1_verify_persons_data():

    curr_index = st.session_state['ar_number_of_person']
    curr_person = st.session_state['ar_persons'][curr_index]

    col1, col2 = st.columns([2, 1])
    with col1:
        st.progress(int(
            (100/len(st.session_state['ar_persons']))*(st.session_state['ar_number_of_person']+1)))
        st.markdown("## Check persons info: ")
        st.markdown(
            f"Person number: &nbsp; &nbsp; **{st.session_state['ar_number_of_person']+1}**")
        st.write(" ")
        st.text_input("🎩 Name", value=curr_person.name_surname,
                        key=f"{curr_index}-name", placeholder="Obligatory")
        st.text_input("🌸 Orcid", value=curr_person.orcid,
                        key=f"{curr_index}-orcid", placeholder="Obligatory")
        st.text_input("🏫 Affiliation", value=curr_person.affiliation,
                        key=f"{curr_index}-affiliation", placeholder="Obligatory")
        if curr_person.calc_kw != ['']:
            st.text_area("🔑 Given Keywords", value=", ".join(
                curr_person.given_kw), key=f"{curr_index}-given_kwords", height=100)
        else:
            st.text_area("🔑 Given Keywords", value=", ".join(curr_person.given_kw),
                            key=f"{curr_index}-given_kwords", placeholder='Optional with found keywords', height=100)
    with col2:
        place = st.empty()
        st.text_area("🔍 Found Keywords", value=", ".join(
            curr_person.calc_kw), key=f"{curr_index}-found_kwords", height=500)
        with place.container():
            if st.session_state['ar_number_of_person'] + 1 < len(st.session_state['ar_persons']):
                if st.session_state[f"{curr_index}-name"].strip() != "" and st.session_state[f"{curr_index}-orcid"].strip() != "" and st.session_state[f"{curr_index}-affiliation"].strip() != "" and (st.session_state[f"{curr_index}-given_kwords"].strip() != "" or st.session_state[f"{curr_index}-found_kwords"].strip() != ""):
                    st.button("Continue", on_click=next_person)
                    st.button("Continue while no conflicts",
                                on_click=next_person_skip)
                else:
                    st.button("Continue", on_click=next_person,
                                disabled=True)
                    st.button("Continue while no conflicts",
                                on_click=next_person_skip, disabled=True)
            else:
                if st.session_state[f"{curr_index}-name"].strip() != "" and st.session_state[f"{curr_index}-orcid"].strip() != "" and st.session_state[f"{curr_index}-affiliation"].strip() != "" and (st.session_state[f"{curr_index}-given_kwords"].strip() != "" or st.session_state[f"{curr_index}-found_kwords"].strip() != ""):
                    st.button("Finish", on_click=move_next_page)
                else:
                    st.button("Finish", on_click=move_next_page,
                                disabled=True)

def source3_get_submission_files():
    st.markdown("Upload a submission file")
    st.file_uploader('Submission', ['.csv'], key="ar_submission_file_raw", on_change=update_submission_file)


def filter2_configure_matching_and_eval_the_scores():

    st.markdown("### Start Evaluation")
    st.write("🔨 Some configurations should be here")
    if 'max_papers_per_person' not in st.session_state:
        st.session_state['max_papers_per_person'] = len(st.session_state['ar_submission_pd'])//len(st.session_state['ar_persons']) + 1
    st.session_state['save_max_papers_per_person'] =  st.number_input("Number of maximum papers for each person",1, len(st.session_state['ar_submission_pd']),key='max_papers_per_person')
    st.number_input("Default number of candidates per page displayed",1, 10,4,key='default_number_of_candidates')
    st.session_state['save_max_candidates_per_paper'] = st.number_input("Max number of persons per doc", 1, len(st.session_state['ar_persons']),1,key='ar_max_candidates_per_paper')
    st.number_input("Min number of persons per doc",1,len(st.session_state['ar_persons']),1,key='min_persons_per_doc')
    st.checkbox("Priority is affected by number of assigned papers",value=False)
    st.checkbox("Normalize number of keywords",value=True,key="normalize_keywords",help="Normalize the value of the vectors to avoid the over-grade by amount of vectors")
    if st.session_state['normalize_keywords']:
        st.slider("Normalization factor",0.0,1.0,0.6,key='norm_factor',help="Meaning is every subsequent keyword will be weighted by a factor less")
    else:
        st.session_state['norm_factor'] = 0
    st.selectbox("Auto-fill method",["Best matches for paper","Best matches for person","Reviewer - Paper best matches"])
    
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


def sink():

    st.markdown(" Paper: "+str(st.session_state['ar_number_of_paper']))

    st.progress(((100/len(st.session_state['result'])) * st.session_state['ar_number_of_paper'])/100)

    if st.session_state['ar_number_of_paper'] < len(st.session_state['result']):
        #
        result = st.session_state['result'][st.session_state['ar_number_of_paper']]

        col1, col2 = st.columns([1, 1])
        with col1:
            
            text = "\n".join(textwrap.wrap(text=result[3], width=40))
            st.write('<div style="position: fixed; overflow-y: scroll; width: 35%;  height: 80vh;">'+f" \n <h2> Assign person  👉  </h2> <div>🌟 Title:  </div><div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{result[1]}</div><div>🔑 Key words:  </div><div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{result[2]}</div><div>🎩 Authors:  </div><div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{result[4]}</div><div>🧾 Abstract:  </div><div>&nbsp;&nbsp;&nbsp;&nbsp;{text}</div>" + " </div>",unsafe_allow_html=True)


        with col2:
            if len(st.session_state['picked_candidates']) >= st.session_state['min_persons_per_doc']:
                st.button("Confirm",on_click=confirm_list_of_candidates)
            else:
                st.button("Confirm",on_click=confirm_list_of_candidates,disabled=True)
            st.button("Auto-fill",on_click=auto_complete_stupid)
            render_candidates()

            st.button("Add more candidates",on_click=add_more_candidates)
    else:
        out_list = []
        for assign in st.session_state['ar_list_of_assigned']:
            out_list.append(
                {"Id": assign[0], "Title": assign[1], "Orcid": assign[5][0].orcid, "Name": assign[5][0].name_surname})
        df = pd.DataFrame.from_dict(out_list)
        out_enc = df.to_csv().encode("utf-8")
        if st.download_button(
            label="Download assignation file",
            data=out_enc,
            file_name='assignment.csv',
            mime='text/csv',
        ):
            st.balloons()


if __name__ == '__main__':

    # WORK FLOW 

    if st.session_state['work_flow_stage'] == 0:

        source1_get_reviewers()

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