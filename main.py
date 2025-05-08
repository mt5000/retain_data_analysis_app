from datetime import datetime
import os

import streamlit as st
import pandas as pd
from google.genai import Client as GeminiClient
from google.genai.types import GenerateContentConfig, Tool, ToolCodeExecution
from google.cloud import bigquery
from google.oauth2 import service_account


gemini = GeminiClient()

def get_bigquery_table(
                        project_id: str = "healthy-dragon-300820",
                        dataset_id: str = "application_analytics",
                        table_id: str = "retain_for_ai_analysis",
                       ) -> pd.DataFrame | None:
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


def get_llm_result(query: str):
    ai_response = gemini.models.generate_content(
        model="gemini-2.0-flash",
        contents=[query,
        ],
        config=GenerateContentConfig(tools=[Tool(code_execution=ToolCodeExecution)])
    )
    return ai_response

st.markdown("<div class='title'>Success Enabler Search & Discovery Feedback Form</div>", unsafe_allow_html=True)


