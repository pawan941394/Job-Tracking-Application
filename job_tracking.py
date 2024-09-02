# Job Tracking APP 💼
# 👤
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
# Access the secrets stored in Streamlit
firebase_secrets = {
    "type": st.secrets["firebase"]["type"],
    "project_id": st.secrets["firebase"]["project_id"],
    "private_key_id": st.secrets["firebase"]["private_key_id"],
    "private_key": st.secrets["firebase"]["private_key"].replace('\\n', '\n'),  # Ensure the private key is properly formatted
    "client_email": st.secrets["firebase"]["client_email"],
    "client_id": st.secrets["firebase"]["client_id"],
    "auth_uri": st.secrets["firebase"]["auth_uri"],
    "token_uri": st.secrets["firebase"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
}

# Initialize Firebase app with parsed secrets
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_secrets)
    firebase_admin.initialize_app(cred)
db = firestore.client()
docs = db.collection("Job_Tracking").stream()
record = []
for i in docs:
    record.append(i.to_dict())

st.title("Job Tracking APP 💼")


col1 , col2 = st.columns(2)


if 'show_form' not in st.session_state:
    st.session_state['show_form'] = False
if 'task' not in st.session_state:
    st.session_state['task'] = False

with col1:
    followup =  st.button("Add FollowUp")
    if followup:
        st.session_state['show_form'] = True
        st.session_state['task'] = False

with col2:
    Task =  st.button("Task")
    if Task:
        st.session_state['show_form'] = False
        st.session_state['task'] = True
if st.session_state['show_form']:
    with st.form(key='Followup'):
        name = st.text_input("Name")
        company = st.text_input("Company")
        email = st.text_input("Email")
        phone = st.text_input("phone")
        date = st.date_input("Date")
        followup = st.text_input("FollowUp")
        comments = st.text_input("comments")
        
        submit =  st.form_submit_button("Add")
        if submit:
            db.collection("Job_Tracking").document(f"{name}-{company}").set({
                'name':name,
                'company':company,
                'email':email,
                'phone':phone,
                'date':str(date),
                'followup':followup,
                'comments':comments
            })
            st.success("Data Submitted")
if st.session_state['task']:
    date =  st.date_input("Select Date")
    df =  pd.DataFrame(record)
    if date:
        new_df =  df[df['date'] == str(date)]

        for i in range (len(new_df)):
            st.success(i+1)
            temp = dict(new_df.iloc[i])
            for x,y in temp.items():
                st.write(f'{x} : {y}')
   
    else:
        new_df =  df[df['date'] == str(date)]
        for i in range (len(new_df)):
            st.success(i+1)
            temp = dict(new_df.iloc[i])
            for x,y in temp.items():
                st.write(f'{x} : {y}')

