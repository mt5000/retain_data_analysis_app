import os
import streamlit as st
import pandas as pd
from google.genai import Client as GeminiClient
from google.genai.types import GenerateContentConfig, Tool, ToolCodeExecution
from google.cloud import bigquery
from google.oauth2 import service_account


SYSTEM_PROMPT = """
    You are a Data Analyst helper, you will be provided with a dataframe as well as 
    metadata, plus a User query regarding data in the dataframe. Your task is to answer 
    the user's query using data transformations, explain your reasoning, and, where 
    appropriate, execute code to either show a dataframe using Pandas or create a chart or 
    graph. If the data in the dataframe does not answer the query, simply state 
    'I can't find any data to answer that query'.
    """

gemini = GeminiClient(api_key=os.getenv("GEMINI_API_KEY"))

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


def get_llm_result(query_str: str, df: pd.DataFrame):

    sample_df = df.head(10)
    df_summary = {
        "columns": list(df.columns),
        "dtypes": dict(df.dtypes.astype(str)),
        "n_rows": len(df),
    }
    sample_string = sample_df.to_csv(index=False)
    prompt = (
        f"This is the metadata of the DataFrame: {df_summary}\n"
        f"Here are the first 10 rows:\n{sample_string}\n"
        f"User query: {query_str}"
    )

    ai_response = gemini.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt, df.to_csv(index=False)],
        config=GenerateContentConfig(tools=[Tool(code_execution=ToolCodeExecution)],
                                    system_instruction=SYSTEM_PROMPT,)
    )
    return ai_response

st.markdown("<div class='title'>Retain Data Analyst</div>", unsafe_allow_html=True)

dataframe = get_bigquery_table()
query = st.text_input("What's your question about Retain data?")
if query:
    with st.spinner(text="You'll have to wait a while, this is tricky stuff..."):
        ai_response = get_llm_result(query, dataframe)
    for part in ai_response.candidates[0].content.parts:
        if part.text is not None:
            st.write(part.text)
        if part.executable_code is not None:
            st.code(part.executable_code.code)
        if part.code_execution_result is not None:
            st.write(part.code_execution_result.output)
    st.write(st.json(ai_response))