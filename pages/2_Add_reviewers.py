import streamlit as st
import pandas as pd
import asyncio

async def call_to_database(person_data):
    await asyncio.sleep(5)
    return None


async def add_reviewer(x):
    await asyncio.sleep(5)
    # print(x['first name'])
    st.write(x['first name'])

    
    st.button('Cont',key=x)


def file_uploaded():

    df_rev = pd.read_csv(st.session_state['ar_reviewers_file'])

    ioloop = asyncio.new_event_loop()
    tasks = [add_reviewer(row[1]) for row in df_rev.iterrows()]
    wait_tasks = asyncio.wait(tasks)
    ioloop.run_until_complete(wait_tasks)
    ioloop.close()

    # for row in df_rev.iterrows():
    #     pass
        # db_answer = call_to_database(person_data = row)


st.markdown("# Load file with Reviewers")


st.file_uploader("Reviewers File ",['.csv'],key='ar_reviewers_file',on_change=file_uploaded)

