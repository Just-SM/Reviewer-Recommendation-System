import streamlit as st
import utils.data_loader
import textwrap

st.set_page_config(layout='wide',
    page_title="RRS Home page",
    page_icon="🎈",)


if 'mt_main_empty' not in st.session_state:
    st.session_state['mt_main_empty'] = st.empty()  

if "mt_data_holder" not in st.session_state:
    st.session_state['mt_data_holder'] = utils.data_loader.DataHolder() 



temp_doc_data = {"title": "Some paper ",
                 "kw": " CV, Networks, Machine Learning",
                 'ab': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut rutrum nisi eget quam consectetur viverra. Nunc id justo non massa varius tempor ullamcorper ut lectus. Suspendisse vestibulum purus at velit tempor pellentesque eu eu nunc. Maecenas et accumsan purus. Mauris elementum nibh eu nibh lacinia accumsan. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Praesent consequat est nunc, eu faucibus justo blandit id. Morbi in efficitur lorem. Pellentesque ultricies neque et velit facilisis, ut faucibus sapien ornare. Donec at ex nulla. Ut lacinia nulla a ex viverra cursus."}




temp_data_reviewers = {"name": "Roman",
                    "surname": "Furzykov",
                    "id": 1,
                    "sim": 0.98,
                    "rw":3,
                    "matching_kw":["Networks","Machine Learning"]}


list_of_docs = [temp_doc_data]

list_of_possible_rew = [temp_data_reviewers]*4



def update_committee():
    
    data = st.session_state['mt_data_holder'].load_committee(st.session_state['mt_committee_raw_file'].getvalue())
    st.dataframe(st.session_state['mt_data_holder'].committee_df)

def update_authors():
    
    data = st.session_state['mt_data_holder'].load_authors(st.session_state['mt_authors_raw_file'].getvalue())
    st.dataframe(st.session_state['mt_data_holder'].authors_df)

def update_submissions():
    
    data = st.session_state['mt_data_holder'].load_submissions(st.session_state['mt_submissions_raw_file'].getvalue())
    st.dataframe(st.session_state['mt_data_holder'].submissions_df)


def prep_revs():
    pass

def perform_search_for_paper(x):
    return list_of_possible_rew

def start_search():


    prep_revs()

    for paper in list_of_docs:

        candidates = perform_search_for_paper(paper)


def format_paper_to_text(paper):
    formated_ab_string = ""
    for line in textwrap.wrap(paper['ab'],width=40):
        formated_ab_string += "|    " + line.ljust(45) + " |\n"
    return(f"""
| -------------------------------------------------|
  🔖 Title :                                       
|   {paper['title'].ljust(47)}|
| -------------------------------------------------|
  🔑Keywords :                                     
|   {paper['kw'].ljust(47)}|
| -------------------------------------------------|
  📖 Abstract :
{formated_ab_string}| -------------------------------------------------|""")


def format_person_to_text(person):
    return(f"""
| ---------------------------------|
  🔖 Name :  
|   {(person['name'] +" "+ person['surname']).ljust(31)}|
| ---------------------------------|
  🔍 Similarity Index :
|   {str(person['sim']).ljust(31)}|
| ---------------------------------|
   🔑 Matching keywords :
|   {", ".join(person['matching_kw']).ljust(31)}|
""")

# side bar config

st.sidebar.markdown("⬆ Upload Files ")


st.sidebar.file_uploader("Upload committee",on_change=update_committee,key='mt_committee_raw_file')

st.sidebar.file_uploader("Upload authors",key='mt_authors_raw_file',on_change=update_authors)

st.sidebar.file_uploader("Upload submissions",key='mt_submissions_raw_file',on_change=update_submissions)




st.markdown("# Start Matching")



if st.session_state['mt_committee_raw_file'] is not None and  st.session_state['mt_authors_raw_file'] is not None and st.session_state['mt_submissions_raw_file'] is not None:
    st.markdown("# Start Matching")

    

else:
    st.markdown(" ne")

    

    bt = st.button("Start")
    if bt:

        paper = temp_doc_data

        list_of_candidates = [temp_data_reviewers]

        col1, col2, col3  = st.columns([2,1,1])

        with col1:
            st.text(format_paper_to_text(paper))

        with col2:
            st.text(format_person_to_text(list_of_candidates[0]))
            st.button("Assign",key='ass1')
            st.text(format_person_to_text(list_of_candidates[0]))
            st.button("Assign",key='ass3')
        
        with col3:
            st.text(format_person_to_text(list_of_candidates[0]))
            st.button("Assign",key='ass2')
            st.text(format_person_to_text(list_of_candidates[0]))
            st.button("Assign",key='ass4')

