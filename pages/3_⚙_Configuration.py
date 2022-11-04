import streamlit as st


st.markdown("> 👈 Don't forget about the sidebar.")

st.markdown("## ⚙ Configuration")


st.markdown(">🐒  Important note: It is configured I a way we think it is performing at its best, If you don't know what is going on here - better not to change here anything)")


st.session_state['gc_work_mode'] = st.selectbox("Work mode: ", ["Hybrid","Semantic meaning + LSH","Keywords set similarity"])

st.markdown("---")

if st.session_state['gc_work_mode'] == "Hybrid":

    st.markdown(" **Weights of usage. Where 0.0 is Most using the LSH + Semantic meaning and the 1.0 is Keywords sets**")
    

    st.slider(" LSH <------------------------------------------------------------------------------------------------------------------------------------> Keywords sets",0.0,1.0,0.3)

    st.markdown("---")

    st.slider("Minimal similarity of result vectors: ",0.0,1.0,0.89)

    st.markdown("---")

    st.slider("Minimal number of keywords: ",1,10,5)

elif st.session_state['gc_work_mode'] == "Semantic meaning + LSH":

    st.slider("Minimal similarity of result vectors: ",1,10,3)

else:

    st.slider("Minimal number of keywords: ",1,10,3)
