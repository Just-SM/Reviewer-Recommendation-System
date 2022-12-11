import streamlit as st

from .common_utils import move_next_page



def next_person():
    st.session_state['ar_number_of_person'] += 1

def next_person_skip():
    
    
    while st.session_state[f"{st.session_state['ar_number_of_person']}-name"].strip() != "" and st.session_state[f"{st.session_state['ar_number_of_person']}-orcid"].strip() != "" and st.session_state[f"{st.session_state['ar_number_of_person']}-affiliation"].strip() != "" and (st.session_state[f"{st.session_state['ar_number_of_person']}-given_kwords"].strip() != "" or st.session_state[f"{st.session_state['ar_number_of_person']}-found_kwords"].strip() != "") and st.session_state['ar_number_of_person']+1 < len(st.session_state['ar_persons']):
        next_person()
        pre_render()


def pre_render():
    curr_index = st.session_state['ar_number_of_person']
    curr_person = st.session_state['ar_persons'][curr_index]

    st.session_state[f"{curr_index}-name"] = curr_person.name_surname
    st.session_state[f"{curr_index}-orcid"] = curr_person.orcid
    st.session_state[f"{curr_index}-affiliation"] = curr_person.affiliation
    st.session_state[f"{curr_index}-given_kwords"] = ", ".join(curr_person.given_kw)
    st.session_state[f"{curr_index}-found_kwords"] = ", ".join(curr_person.calc_kw)

def update_info():
    curr_index = st.session_state['ar_number_of_person']
    curr_person = st.session_state['ar_persons'][curr_index]

    curr_person.name_surname = st.session_state[f"{curr_index}-name"]
    curr_person.orcid = st.session_state[f"{curr_index}-orcid"]
    curr_person.affiliation = st.session_state[f"{curr_index}-affiliation"] 
    curr_person.given_kw =  st.session_state[f"{curr_index}-given_kwords"].split(", ")
    curr_person.calc_kw = st.session_state[f"{curr_index}-found_kwords"].split(", ")

def filter1_verify_persons_data():

    if 'ar_number_of_person' not in st.session_state:
        st.session_state['ar_number_of_person'] = 0
    
    curr_index = st.session_state['ar_number_of_person']
    curr_person = st.session_state['ar_persons'][curr_index]

    pre_render()

    col1, col2 = st.columns([2, 1])
    with col1:
        st.progress(int(
            (100/len(st.session_state['ar_persons']))*(st.session_state['ar_number_of_person']+1)))
        st.markdown("## Check persons info: ")
        st.markdown(
            f"Person number: &nbsp; &nbsp; **{st.session_state['ar_number_of_person']+1}**")
        st.write(" ")
        st.text_input("🎩 Name", 
                    key=f"{curr_index}-name", placeholder="Obligatory",on_change=update_info)
        st.text_input("🌸 Orcid", 
                        key=f"{curr_index}-orcid", placeholder="Obligatory",on_change=update_info)
        st.text_input("🏫 Affiliation", 
                        key=f"{curr_index}-affiliation", placeholder="Obligatory",on_change=update_info)

        if curr_person.calc_kw != ['']:
            st.text_area("🔑 Given Keywords",  key=f"{curr_index}-given_kwords",on_change=update_info, height=100)
        else:
            st.text_area("🔑 Given Keywords", 
                            key=f"{curr_index}-given_kwords", placeholder='Optional with found keywords',on_change=update_info, height=100)
    with col2:
        place = st.empty()
        st.text_area("🔍 Found Keywords",  key=f"{curr_index}-found_kwords", height=500,on_change=update_info)
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


    # st.stop()
    
    # col1, col2 = st.columns([2, 1])
    # with col1:
    #     st.progress(int(
    #         (100/len(st.session_state['ar_persons']))*(st.session_state['ar_number_of_person']+1)))
    #     st.markdown("## Check persons info: ")
    #     st.markdown(
    #         f"Person number: &nbsp; &nbsp; **{st.session_state['ar_number_of_person']+1}**")
    #     st.write(" ")
    #     st.text_input("🎩 Name", value=curr_person.name_surname,
    #                 key=f"{curr_index}-name", placeholder="Obligatory")
    #     st.text_input("🌸 Orcid", value=curr_person.orcid,
    #                     key=f"{curr_index}-orcid", placeholder="Obligatory")
    #     st.text_input("🏫 Affiliation", value=curr_person.affiliation,
    #                     key=f"{curr_index}-affiliation", placeholder="Obligatory")

    #     if curr_person.calc_kw != ['']:
    #         st.text_area("🔑 Given Keywords", value=", ".join(
    #             curr_person.given_kw), key=f"{curr_index}-given_kwords", height=100)
    #     else:
    #         st.text_area("🔑 Given Keywords", value=", ".join(curr_person.given_kw),
    #                         key=f"{curr_index}-given_kwords", placeholder='Optional with found keywords', height=100)
    # with col2:
    #     place = st.empty()
    #     st.text_area("🔍 Found Keywords", value=", ".join(
    #         curr_person.calc_kw), key=f"{curr_index}-found_kwords", height=500)
    #     with place.container():
    #         if st.session_state['ar_number_of_person'] + 1 < len(st.session_state['ar_persons']):
    #             if st.session_state[f"{curr_index}-name"].strip() != "" and st.session_state[f"{curr_index}-orcid"].strip() != "" and st.session_state[f"{curr_index}-affiliation"].strip() != "" and (st.session_state[f"{curr_index}-given_kwords"].strip() != "" or st.session_state[f"{curr_index}-found_kwords"].strip() != ""):
    #                 st.button("Continue", on_click=next_person)
    #                 st.button("Continue while no conflicts",
    #                             on_click=next_person_skip)
    #             else:
    #                 st.button("Continue", on_click=next_person,
    #                             disabled=True)
    #                 st.button("Continue while no conflicts",
    #                             on_click=next_person_skip, disabled=True)
    #         else:
    #             if st.session_state[f"{curr_index}-name"].strip() != "" and st.session_state[f"{curr_index}-orcid"].strip() != "" and st.session_state[f"{curr_index}-affiliation"].strip() != "" and (st.session_state[f"{curr_index}-given_kwords"].strip() != "" or st.session_state[f"{curr_index}-found_kwords"].strip() != ""):
    #                 st.button("Finish", on_click=move_next_page)
    #             else:
    #                 st.button("Finish", on_click=move_next_page,
    #                             disabled=True)