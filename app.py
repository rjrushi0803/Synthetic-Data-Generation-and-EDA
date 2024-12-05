import streamlit as st
import numpy as np
import pandas as pd
import pickle

## importing a ML model
with open('gradient_boost_model.pkl','rb') as f:
    gb_model = pickle.load(f)

with open('job_encoder.pkl', 'rb') as f:
    enc_job = pickle.load(f)
with open('location_encoder.pkl', 'rb') as f:
    enc_loc = pickle.load(f)

st.title("Hourly Pay Rate Prediction")

st.header("Enter the details below:")
job_title = st.selectbox(
    "Job Title", 
    options=["RegisteredNurse_ICU", "RegisteredNurse_MedSurg", "RegisteredNurse_Telemetry",
        "RegisteredNurse_Oncology", "RegisteredNurse_Pediatric", "PhysioTherapist",
        "LabTechnician", "RegisteredNurse_CriticalCare", "RegisteredNurse_Cardiology",
        "RegisteredNurse_Surgery"],
    help="Select the job title from the dropdown."
)

location = st.selectbox(
    "Location", 
    options=["Dallas", "Atlanta", "New York", "Philadelphia", "Washington", "San Francisco",
        "Los Angeles", "Seattle", "Chicago", "San Diego", "Miami", "Boston",
        "Detroit", "Phoenix", "Houston"],
    help="Select the Location from the dropdown."
)
hospital_name = st.text_input("Hospital Name",help="Enter Hospital Name (EX: Chicago Veterans)")
contract_start = st.date_input("Contract Start Date")
contract_end = st.date_input("Contract End Date")

u_df = {'Job_Title':[job_title], 'Location':[location], 'Hospital_Name':[hospital_name], 'Contract_Start_Date':[contract_start],'Contract_End_Date':[contract_end]}
user_df = pd.DataFrame(u_df)
user_df.Location = user_df.Location.apply(lambda x: x.replace(' ','_'))

user_df['Contract_Start_Date'] = pd.to_datetime(user_df['Contract_Start_Date'])
user_df['Contract_End_Date'] = pd.to_datetime(user_df['Contract_End_Date'])
user_df['start_day'] = user_df['Contract_Start_Date'].apply(lambda x: x.day)
user_df['start_month'] = user_df['Contract_Start_Date'].apply(lambda x: x.month)
user_df['start_year'] = user_df['Contract_Start_Date'].apply(lambda x: x.year)

user_df['end_day'] = user_df['Contract_End_Date'].apply(lambda x: x.day)
user_df['end_month'] = user_df['Contract_End_Date'].apply(lambda x: x.month)
user_df['end_year'] = user_df['Contract_End_Date'].apply(lambda x: x.year)

u_job_title_encoded = enc_job.transform(user_df[['Job_Title']]).toarray()
u_encoded_df = pd.DataFrame(u_job_title_encoded, columns=enc_job.get_feature_names_out(['Job_Title']))

u_loc_title_encoded = enc_loc.transform(user_df[['Location']]).toarray()
u_encoded_df = pd.concat([u_encoded_df,pd.DataFrame(u_loc_title_encoded, columns=enc_loc.get_feature_names_out(['Location']))], axis= 1)

df_enc = pd.concat([u_encoded_df,user_df[['start_day','start_month', 'start_year', 'end_day', 'end_month', 'end_year']]],axis = 1)


# Dummy model prediction
if st.button("Predict Hourly Pay Rate"):
    prediction = gb_model.predict(df_enc)
    st.success(f"The predicted Hourly Pay Rate is: ${prediction[0]:.2f}")
