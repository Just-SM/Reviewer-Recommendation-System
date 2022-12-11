import streamlit as st
import textwrap
import pandas as pd


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
            while len(pack) < st.session_state['save_min_persons_per_doc']:
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

    st.session_state['ar_number_of_paper'] = len(st.session_state['result'])


def confirm_list_of_candidates():
    for confirmed in st.session_state['picked_candidates']:
        st.session_state['ar_list_of_assigned'].append(confirmed)
        st.session_state['ar_dict_of_number_assignments'][confirmed[5][0].orcid] = st.session_state['ar_dict_of_number_assignments'][confirmed[5][0].orcid] + 1 

    for x in range (st.session_state['number_of_candidates_per_paper'][st.session_state['ar_number_of_paper']]):
        st.session_state[f'p{x}'] = False

    st.session_state['ar_number_of_paper'] += 1
    st.session_state['picked_candidates'] = []


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



def sink():

    if 'ar_dict_of_number_assignments' not in st.session_state:
        st.session_state['ar_dict_of_number_assignments'] = dict()
    if 'picked_candidates' not in st.session_state:
        st.session_state['picked_candidates'] = []
    if 'ar_list_of_assigned'not in st.session_state:
        st.session_state['ar_list_of_assigned'] = []
    if 'ar_number_of_paper' not in st.session_state:
        st.session_state['ar_number_of_paper'] = 0

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
            if len(st.session_state['picked_candidates']) >= st.session_state['save_min_persons_per_doc']:
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