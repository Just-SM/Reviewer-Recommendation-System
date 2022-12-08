import streamlit as st

st.set_page_config(
    page_title="Configure Reviewers",
    page_icon="🎩",)




    
st.session_state['reviewers'] = [["Jan","Kowalski",["CS","Math"]],["Jroslaw","Kovalskiy",["Bio","Chemistry"]]]
st.session_state['topics'] = ["CS","Bio","Math",'Sports','Chemistry']

if 'current_display' not in st.session_state    :
    st.session_state['current_display'] = st.session_state['reviewers']



def update_list():
    st.session_state['current_display'] = [s for s in st.session_state['reviewers'] if st.session_state['search_bar'].lower() in s[0].lower()]


st.session_state['reviewers'] = [["Jan","Kowalski",["CS","Math"]],["Jroslaw","Kovalskiy",["Bio","Chemistry"]]]
st.session_state['topics'] = ["CS","Bio","Math",'Sports','Chemistry']

st.text_input("🔍Search",placeholder="Search for Name",key="search_bar",on_change=update_list)

if "reviewers" in st.session_state:
    for ind in range(100):

        for rew in st.session_state['current_display']:
            
            with st.expander(f"{rew[0]} {rew[1]}"):
                rew[2] = st.multiselect("Topics :",st.session_state['topics'],rew[2],key=f"{rew[0]}_{rew[1]}_topics {ind}")
            
                check = st.checkbox("Show shadow keywords",False,key=f"{rew[0]}_{rew[1]}_check {ind}")
                if check:
                    rew[2] = st.multiselect("Shadow Topics :",st.session_state['topics'],st.session_state['topics'],key=f"{rew[0]}_{rew[1]}_shadow {ind}")

else:
    st.markdown("## NO reviewers are uploaded yet")
