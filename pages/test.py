import streamlit as st


def res():
    st.session_state['1'] =False
    st.session_state['2'] =False
    st.session_state['3'] =False



st.checkbox("dqwdqwd",key='1')
st.checkbox("dqwdqwd",key='2')
st.checkbox("dqwdqwd",key='3')

st.button("reset",on_click=res)