import streamlit as st
import pandas as pd
from gpt4all import GPT4All
from langchain_community.llms import GPT4All
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType

# Page title
st.set_page_config(page_title='🦜🔗 Ask the Data App')
st.title('🦜🔗 Ask the Data App')

# Load CSV file
def load_csv(input_csv):
  df = pd.read_csv(input_csv)
  with st.expander('See DataFrame'):
    st.write(df)
  return df

# Generate LLM response
def generate_response(csv_file, input_query):

  llm = GPT4All(model="C:/Users/gsdav/AppData/Local/nomic.ai/GPT4All/Meta-Llama-3-8B-Instruct.Q4_0.gguf")
  df = load_csv(csv_file)
  # Create Pandas DataFrame Agent
  agent = create_pandas_dataframe_agent(llm, df, verbose=True)
  # Perform Query using the Agent
  response = agent.invoke(input_query)
  return st.success(response)

# Input widgets
uploaded_file = st.file_uploader('Upload a CSV file', type=['csv'])
question_list = [
  'How many rows are there?',
  'What is the range of values is greater than 0?',
  'How many rows have a value greater than 0.',
  'Other']
query_text = st.selectbox('Select an example query:', question_list, disabled=not uploaded_file)

# App logic
if query_text == 'Other':
  query_text = st.text_input('Enter your query:', placeholder = 'Enter query here ...', disabled=not uploaded_file)
  st.header('Output')
  generate_response(uploaded_file, query_text)