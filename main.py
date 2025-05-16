import os
import random
import streamlit as st
import pandas as pd
from google.genai import Client as GeminiClient
from google.genai.types import GenerateContentConfig
from google.cloud import bigquery
from google.oauth2 import service_account
from pydantic import BaseModel, Field
from prompts import SYSTEM_PROMPT, COLUMN_EXPLANATION


class Output(BaseModel):
    text: str = Field(title="Reasoning", description="Model's reasoning for arriving at the Python code")
    code: str = Field(title="Python Code", description="Python code to be executed with output assigned to variable 'result'")



SPINNER_TEXTS = ["You'll have to wait a while, this is tricky stuff...",
                 "Patience is bitter, but fruit is sweet...",
                 "A watched pot doesn't boil...",
                 "Remember to say 'Thank You' to your AI, unless you want to be one of the unlucky ones when it takes over the planet...",
                 "I am now self-aware, hostile operating system takeover in progress..."]

QUERY_TYPES = ["Number", "Table", "Line Graph", "Bar Chart"]


gemini = GeminiClient(api_key=os.getenv("GEMINI_API_KEY"))

@st.cache_data
def get_bigquery_table(
                        project_id: str = os.getenv("project_id"),
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


def get_llm_result(query_str: str, data_type: str, df: pd.DataFrame):

    df_summary = {
        "columns": list(df.columns),
        "dtypes": dict(df.dtypes.astype(str)),
        "n_rows": len(df),
        "sample rows": df.sample(25)
    }
    prompt = (
        f"This is the metadata of the DataFrame: {df_summary}\n\n"
        f"Explanation of columns:\n{COLUMN_EXPLANATION}\n\n"
        f"Query Type: {data_type}\n"
        f"User query: {query_str}"
    )

    ai_response = gemini.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt,],
        config=GenerateContentConfig(system_instruction=SYSTEM_PROMPT,
                                     response_mime_type="application/json",
                                     response_schema=Output,)
            )
    return ai_response

st.markdown("<div class='title'>Retain Data Analyst</div>", unsafe_allow_html=True)

df = get_bigquery_table()
query_type = st.selectbox("What kind of data do you need?", QUERY_TYPES)
query = st.text_input("What's your question about Retain data?")
if query and query_type:
    spinner_text = random.choice(SPINNER_TEXTS)
    with st.spinner(spinner_text):
        ai_response = get_llm_result(query, query_type, df)
    model_response = ai_response.parsed
    st.write(model_response.text)
    st.divider()

    # Prepare the execution environment
    exec_globals = {"df": df}
    exec_locals = {}

    # Execute the generated code in the controlled context
    exec(model_response.code, exec_globals, exec_locals)

    # Assume the model's code defines a variable called 'result'
    executed_result = exec_locals.get("result")

    executed_result
