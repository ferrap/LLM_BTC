import os 
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
import streamlit as st
from streamlit_chat import message
import pandas as pd
import requests
from langchain.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.DataFrame()
URL = 'https://min-api.cryptocompare.com/data/histoday?fsym=ETH&tsym=USD&allData=true' 
res = requests.get(URL)
res_json = res.json()
data= res_json['Data']
temp_df= pd.DataFrame(data)
temp_df['conversionSymbol']= 'USD'
df = pd.concat([df,temp_df], ignore_index=True)
df['time']=pd.to_datetime(df['time'],unit='s')
df['time'] = df['time'].dt.strftime('%d/%m/%Y')


import streamlit as st
from streamlit_chat import message

from langchain.chains import ConversationChain
from langchain.llms import OpenAI

open_ai_key = st.secrets["OPENAI_API_KEY"]

llm = ChatOpenAI(temperature=0)
agent = create_pandas_dataframe_agent(llm, df, verbose=True)

# Setup streamlit app
# Display the page title and the text box for the user to ask the question
st.title('✨ Query your Data ')
prompt = st.text_input("Enter your question to query your PDF documents")


if prompt:
    # Get the resonse from LLM
    # We pass the model name (3.5) and the temperature (Closer to 1 means creative resonse)
    # stuff chain type sends all the relevant text chunks from the document to LLM

    response =  agent.run(prompt)


    # Write the results from the LLM to the UI
    #st.write("<b>" + prompt + "</b><br><i>" + response + "</i><hr>", unsafe_allow_html=True )
    st.write(response)
