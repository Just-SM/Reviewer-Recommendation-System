import streamlit as st
import utils.utils
import pandas as pd
import utils.utils as utl
import textwrap

def display_person(person:utl.PersonData):
    formated_ab_string = ""
    for line in textwrap.wrap(", ".join([x[0] for x in person.calc_kw]).ljust(31),width=70):
        formated_ab_string += "|    " + line.ljust(72) + " |\n"
    return(f"""
| ---------------------------------|
  🎩 Name :  
|   {(person.name_surname).ljust(31)}|
| ---------------------------------|
  🌸 Orcid :
|   {str(person.orcid).ljust(31)}|
| ---------------------------------|
  🔑 Keywords :
|   {", ".join(person.given_kw).ljust(31)}|
| ---------------------------------|
  📰 Found Keywords :
{formated_ab_string}| ---------------------------------|
  🏫 Affiliation :
|   {str(person.affiliation).ljust(31)}|

""")

def get_labels_from_person(person):
    titles = st.session_state['dh'].get_titles_by_person(person)
    kwords = []
    for elem in titles:
        kwords.extend(st.session_state['mp'].extract_kw(elem[0]))
    return kwords


if 'dh' not in st.session_state:
    try:
        st.session_state['dh'] = utl.DataHolder()
    except Exception as e:
        print(e)
        st.warning("Can't connect to the database, check your connection and try again later")
if 'mp' not in st.session_state:
    st.session_state['mp'] = utl.Modelprovider()

def update_list():
    res = st.session_state['dh'].get_user_data_by_orcid(st.session_state['text_in'])
    res.calc_kw = get_labels_from_person(res)
    st.text(display_person(res))
    # print(res)
    # kwords = []
    # for elem in res:
    #     kwords.extend(st.session_state['mp'].extract_kw(elem[0]))
    # st.dataframe(pd.DataFrame(kwords,columns=['Kword','Score']).sort_values("Score",ascending=False),use_container_width=True)

st.text_input("ORCID",key='text_in',on_change=update_list)