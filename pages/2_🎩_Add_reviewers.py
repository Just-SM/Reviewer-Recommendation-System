import streamlit as st
import pandas as pd
import utils.utils as utl
from time import sleep
from subprocess import Popen, PIPE
import sys
import json
import textwrap

st.set_page_config(
    page_title="Add Reviewers",
    page_icon="🎩",
    layout='wide')

# CREATE STATE VARS
if 'ar_all_loaded' not in st.session_state:
    st.session_state['ar_all_loaded'] = False

# if 'dh' not in st.session_state:
#     try:
#         st.session_state['dh'] = utl.DataHolder()
#     except Exception as e:
#         print(e)
#         st.warning("Can't connect to the database, check your connection and try again later")
if 'mp' not in st.session_state:
    st.session_state['mp'] = utl.Modelprovider()
if 'ar_accept_person_mode' not in st.session_state:
    st.session_state['ar_accept_person_mode'] = False
if 'ar_number_of_person' not in st.session_state:
    st.session_state['ar_number_of_person'] = 0
if 'ar_get_the_orcids'not in st.session_state:
    st.session_state['ar_get_the_orcids'] = True
if 'ar_assigning_load' not in st.session_state:
    st.session_state['ar_assigning_load'] = False
if 'ar_assigning_config' not in st.session_state: 
    st.session_state['ar_assigning_config'] = False
if 'ar_assigning' not in st.session_state:
    st.session_state['ar_assigning'] = False
if 'ar_number_of_paper' not in st.session_state:
    st.session_state['ar_number_of_paper'] = 0
if 'ar_list_of_assigned'not in st.session_state:
    st.session_state['ar_list_of_assigned'] = []
if 'ar_dict_of_number_assignments' not in st.session_state:
    st.session_state['ar_dict_of_number_assignments'] = dict()
# DEF FUNCTIONS

def evaluate_candidates():
    st.session_state['mp'].prep_papers(st.session_state['ar_submission_pd'])
    st.session_state['mp'].prep_persons(st.session_state['ar_persons'])


def get_persons_form_orcid(orcid):
    return st.session_state['dh'].get_user_data_by_orcid(orcid)

def next_person():
    st.session_state['ar_number_of_paper'] += 1

def next_person():
    st.session_state['ar_number_of_person'] += 1

def next_person_skip():
    while st.session_state[f"{curr_index}-name"].strip() != "" and st.session_state[f"{curr_index}-orcid"].strip() != "" and st.session_state[f"{curr_index}-affiliation"].strip() != "" and (st.session_state[f"{curr_index}-given_kwords"].strip() != "" or st.session_state[f"{curr_index}-found_kwords"].strip() != "" ) and st.session_state['ar_number_of_person']+1 < len(st.session_state['ar_persons']):
       next_person() 

def change_page_to_ass_load():
    st.session_state['ar_all_loaded'] = False
    st.session_state['ar_assigning_load'] = True

def file_uploaded():

    df_rev = st.session_state['ar_reviewers_file'].getvalue().decode("utf-8")
    st.session_state['ar_orcid_ids'] = [x.strip() for x in df_rev.split("\n")]
    st.session_state['ar_accept_person_mode'] =True

def update_submission_file():
    st.session_state['ar_submission_pd'] = pd.read_csv(st.session_state['ar_submission_file_raw'],index_col=['#'])
    st.session_state['ar_submission_pd'] = st.session_state['ar_submission_pd'][["title",'keywords','abstract']]
    st.session_state['ar_assigning_load'] = False
    st.session_state['ar_assigning_config'] = True


def get_the_orcids():

    st.markdown("# Load file with Reviewers")

    st.file_uploader("Reviewers File ",['.txt'],key='ar_reviewers_file',on_change=file_uploaded)

    st.session_state['ar_get_the_orcids'] = False

def assign_person_0():
    result = st.session_state['result'][st.session_state['ar_number_of_paper']]
    st.session_state['ar_list_of_assigned'].append((result[0],result[1],result[2],result[3],result[4][0]))
    st.session_state['ar_number_of_paper'] += 1
    if result[4][0][0].orcid in  st.session_state['ar_dict_of_number_assignments']:
        st.session_state['ar_dict_of_number_assignments'][result[4][0][0].orcid] += 1
    else:
        st.session_state['ar_dict_of_number_assignments'][result[4][0][0].orcid] = 1

def assign_person_1():
    result = st.session_state['result'][st.session_state['ar_number_of_paper']]
    st.session_state['ar_list_of_assigned'].append((result[0],result[1],result[2],result[3],result[4][1]))
    st.session_state['ar_number_of_paper'] += 1
    if result[4][1][0].orcid in  st.session_state['ar_dict_of_number_assignments']:
        st.session_state['ar_dict_of_number_assignments'][result[4][1][0].orcid] += 1
    else:
        st.session_state['ar_dict_of_number_assignments'][result[4][1][0].orcid] = 1    

def assign_person_2():
    result = st.session_state['result'][st.session_state['ar_number_of_paper']]
    st.session_state['ar_list_of_assigned'].append((result[0],result[1],result[2],result[3],result[4][2]))
    st.session_state['ar_number_of_paper'] += 1
    if result[4][2][0].orcid in  st.session_state['ar_dict_of_number_assignments']:
        st.session_state['ar_dict_of_number_assignments'][result[4][2][0].orcid] += 1
    else:
        st.session_state['ar_dict_of_number_assignments'][result[4][2][0].orcid] = 1
def assign_person_3():
    result = st.session_state['result'][st.session_state['ar_number_of_paper']]
    st.session_state['ar_list_of_assigned'].append((result[0],result[1],result[2],result[3],result[4][3]))
    st.session_state['ar_number_of_paper'] += 1
    if result[4][3][0].orcid in  st.session_state['ar_dict_of_number_assignments']:
        st.session_state['ar_dict_of_number_assignments'][result[4][3][0].orcid] += 1
    else:
        st.session_state['ar_dict_of_number_assignments'][result[4][0][0].orcid] = 1

if __name__ == '__main__':

    if st.session_state['ar_get_the_orcids']:
        get_the_orcids()

    if st.session_state['ar_accept_person_mode']:
        
        st.session_state['ar_persons'] = []

        commands = []

        for orcid in st.session_state['ar_orcid_ids']:
            commands.append(str(sys.executable) + r" utils\utils.py " + str(orcid))
            # p = Popen(str(sys.executable) + r" utils\utils.py " + str(orcid),text=True, stdout=PIPE)
            # p.wait()
            # print(p.communicate()[0])
        with st.spinner("Loading data from DataBase"):
            procs = [ Popen(i,text=True, stdout=PIPE) for i in commands]
            for p in procs:
                p.wait()
            for p in procs:
                data_person_raw = json.loads(p.communicate()[0])
                kwords_form_title = None
                if data_person_raw['4'] is not None:
                    kwords_form_title = []
                    for title in data_person_raw['4']:
                        kwords_form_title.extend([x[0]for x in st.session_state['mp'].extract_kw(title[0])])
                st.session_state['ar_persons'].append(utl.PersonData(data_person_raw['1'],data_person_raw['0'],data_person_raw['3'],kwords_form_title,data_person_raw['2']))


        print(st.session_state['ar_accept_person_mode'])
        # load all persons 
        st.session_state['ar_all_loaded'] = True
        st.session_state['ar_accept_person_mode'] = False

    if st.session_state['ar_all_loaded']:

        curr_index = st.session_state['ar_number_of_person']
        curr_person = st.session_state['ar_persons'][curr_index]

        

        col1,col2 = st.columns([2,1])
        with col1:
            # st.progress(int((len(st.session_state['ar_persons'])/st.session_state['ar_number_of_person'])*10))
            st.progress(int((100/len(st.session_state['ar_persons']))*(st.session_state['ar_number_of_person']+1)))
            st.markdown("## Check persons info: ")
            st.markdown(f"Person number: &nbsp; &nbsp; **{st.session_state['ar_number_of_person']+1}**")
            st.write(" ")
            st.text_input("🎩 Name",value=curr_person.name_surname,key=f"{curr_index}-name")
            st.text_input("🌸 Orcid",value=curr_person.orcid,key=f"{curr_index}-orcid")
            st.text_input("🏫 Affiliation",value=curr_person.affiliation,key=f"{curr_index}-affiliation")
            if curr_person.calc_kw != ['']:
                st.text_area("🔑 Given Keywords",value=", ".join(curr_person.given_kw),key=f"{curr_index}-given_kwords",height=100)
            else:
                st.text_area("🔑 Given Keywords",value=", ".join(curr_person.given_kw),key=f"{curr_index}-given_kwords",placeholder='Optional with found keywords',height=100)
        with col2:
            place = st.empty()
            st.text_area("🔍 Found Keywords",value=", ".join(curr_person.calc_kw),key=f"{curr_index}-found_kwords",height=500)
            with place.container():
                if st.session_state['ar_number_of_person'] + 1 < len(st.session_state['ar_persons']):
                    if st.session_state[f"{curr_index}-name"].strip() != "" and st.session_state[f"{curr_index}-orcid"].strip() != "" and st.session_state[f"{curr_index}-affiliation"].strip() != "" and (st.session_state[f"{curr_index}-given_kwords"].strip() != "" or st.session_state[f"{curr_index}-found_kwords"].strip() != "" ): 
                        st.button("Continue",on_click=next_person)
                        st.button("Continue while no conflicts", on_click=next_person_skip)
                    else:
                        st.button("Continue",on_click=next_person,disabled=True)
                        st.button("Continue while no conflicts", on_click=next_person_skip,disabled=True)   
                else:
                    st.button("Finish",on_click=change_page_to_ass_load)




    if st.session_state['ar_assigning_load']:
        st.file_uploader('Submission',['.csv'],key="ar_submission_file_raw",on_change=update_submission_file)
        



    if st.session_state['ar_assigning_config']:
        st.markdown("Start Evaluation")
        st.write("some config")

        if st.button("Start"):
            with st.spinner("Loading the model"):
                st.session_state['mp'].load_vectorizer()
            with st.spinner("Loading the papers"):
                evaluate_candidates()
            with st.spinner("Evaluating the candidates"):
                st.session_state['result'] = []
                for ind,paper in  st.session_state['ar_submission_pd'].iterrows():
                    # st.write(paper)
                    st.session_state['result'].append((ind,paper['title'],paper['keywords'],paper['abstract'],st.session_state['mp'].find_matches_for_paper(paper)))

            st.session_state['ar_assigning_config'] = False
            st.session_state['ar_assigning'] = True
            st.experimental_rerun()


    if st.session_state['ar_assigning']:

            if st.session_state['ar_number_of_paper'] < len(st.session_state['result']):
                # 
                result = st.session_state['result'][st.session_state['ar_number_of_paper']]
                
                col1,col2 = st.columns([1,1])
                with col1:
                    st.progress(int((100/len( st.session_state['result']))*(st.session_state['ar_number_of_paper']+1)))
                    st.markdown("### Assign person  👉")
                    st.markdown(f"🌟 Title:  \n{result[1]}")
                    text = "\n".join(textwrap.wrap(text=result[3],width=40))
                    st.markdown(f"🧾 Abstract:  \n{text}")
                    st.markdown(f"🔑 Key words:  \n{result[2]}")

                with col2:
                    if len(result[4]) >= 1:
                        if result[4][0][0].orcid not in st.session_state['ar_dict_of_number_assignments']:
                            st.session_state['ar_dict_of_number_assignments'][result[4][0][0].orcid] = 0
                        st.markdown(f"🎩 Name: {result[4][0][0].name_surname}  \nPapers : {st.session_state['ar_dict_of_number_assignments'][result[4][0][0].orcid]}  \n 🏫 Affiliation: {result[4][0][0].affiliation}  \n🌟 Score: {'{:.3f}'.format(result[4][0][1])}")
                        st.button("Assign this person",key="assign_person_1",on_click=assign_person_0,type="primary")
                    if len(result[4]) >= 2:
                        if result[4][1][0].orcid not in st.session_state['ar_dict_of_number_assignments']:
                            st.session_state['ar_dict_of_number_assignments'][result[4][1][0].orcid] = 0
                        st.markdown(f"🎩 Name: {result[4][1][0].name_surname}  \nPapers : {st.session_state['ar_dict_of_number_assignments'][result[4][1][0].orcid]}  \n 🏫 Affiliation: {result[4][1][0].affiliation}  \n🌟 Score: {'{:.3f}'.format(result[4][1][1])}")
                        st.button("Assign this person",key="assign_person_2",on_click=assign_person_1)
                    if len(result[4]) >= 3:
                        if result[4][2][0].orcid not in st.session_state['ar_dict_of_number_assignments']:
                            st.session_state['ar_dict_of_number_assignments'][result[4][2][0].orcid] = 0                    
                        st.markdown(f"🎩 Name: {result[4][2][0].name_surname}  \nPapers : {st.session_state['ar_dict_of_number_assignments'][result[4][2][0].orcid]}  \n 🏫 Affiliation: {result[4][2][0].affiliation}  \n🌟 Score: {'{:.3f}'.format(result[4][2][1])}")
                        st.button("Assign this person",key="assign_person_3",on_click=assign_person_2)
                    if len(result[4]) >= 4:
                        if result[4][3][0].orcid not in st.session_state['ar_dict_of_number_assignments']:
                            st.session_state['ar_dict_of_number_assignments'][result[4][3][0].orcid] = 0                    
                        st.markdown(f"🎩 Name: {result[4][3][0].name_surname}  \nPapers : {st.session_state['ar_dict_of_number_assignments'][result[4][3][0].orcid]}  \n 🏫 Affiliation: {result[4][3][0].affiliation}  \n🌟 Score: {'{:.3f}'.format(result[4][3][1])}")
                        st.button("Assign this person",key="assign_person_4",on_click=assign_person_3)

                    if st.button("Assign automatically"):
                        while st.session_state['ar_number_of_paper'] < len(st.session_state['result']):
                            assign_person_0()
                        st.experimental_rerun()
            else:
                    out_list = []
                    for assign in st.session_state['ar_list_of_assigned']:
                        out_list.append({"Id":assign[0],"Title":assign[1],"Orcid":assign[4][0].orcid,"Name":assign[4][0].name_surname})
                    df = pd.DataFrame.from_dict(out_list)
                    out_enc = df.to_csv().encode("utf-8")
                    st.download_button(
                    label="Download assignation file",
                    data=out_enc,
                    file_name='assignment.csv',
                    mime='text/csv',
)
