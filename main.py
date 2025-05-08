from datetime import datetime
import os

import streamlit as st
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account


def get_bigquery_table(
    project_id: str = "healthy-dragon-300820",
    dataset_id: str = "application_analytics",
    table_id: str = "retain_for_ai_analysis",
):
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_credentials"]
    )
    try:
        client = bigquery.Client(credentials=credentials, project=project_id)
        table_ref = f"{project_id}.{dataset_id}.{table_id}"
        query = f"SELECT * FROM `{table_ref}`"
        df = client.query(query).to_dataframe()
        return df
    except Exception as e:
        st.write(e)
        return None


st.markdown("<div class='title'>Success Enabler Search & Discovery Feedback Form</div>", unsafe_allow_html=True)


