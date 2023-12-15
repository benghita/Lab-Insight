# Import necessary libraries
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
import pandas as pd
from fpdf import FPDF
import os 

os.environ['OPENAI_API_KEY'] = "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"

st.set_page_config(
   page_title="Lab Insight",
   page_icon="🔬",
   #layout="wide",
   initial_sidebar_state="expanded",
)

# Load the Excel file with field, subfield, measure, etc.
excel_file_path = "./data.csv"
df = pd.read_csv(excel_file_path, sep=";")

# Streamlit app layout
def main():

    st.title(':microscope: Lab :blue[Insight]')


if __name__ == "__main__":
    main()