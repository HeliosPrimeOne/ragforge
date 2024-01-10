import streamlit as st
import torch
import shutil
import signal
import psutil
import time
import os
import subprocess
import openai
from langchain_openai import OpenAI
from langchain_community.vectorstores import Chroma
from constants import CHROMA_SETTINGS, EMBEDDING_MODEL_NAME, PERSIST_DIRECTORY
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.chains import RetrievalQA
from streamlit_extras import add_vertical_space as avs
import warnings
from langchain_core._api.deprecation import LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning) ##Using Latest Langchain Version 0.1.0 which causes error msg. Will update if code breaks.

def load_remote_model(api_key, base_url):
    openai.api_key = api_key
    openai.base_url = base_url

if torch.backends.mps.is_available():
    DEVICE_TYPE = "mps"
elif torch.cuda.is_available():
    DEVICE_TYPE = "cuda"
else:
    DEVICE_TYPE = "cpu"

def save_uploadedfile(uploadedfile):
    with open(os.path.join("SOURCE_DOCUMENTS", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    st.success("Saved File: {} to SOURCE_DOCUMENTS".format(uploadedfile.name))

def delete_db_folder():
    db_folder_path = os.path.join(os.getcwd(), "DB")
    if os.path.exists(db_folder_path):
        shutil.rmtree(db_folder_path)
        st.success("Deleted 'DB' folder")    
        return db_folder_path

st.markdown("🌞 RAGForge - Rag-Powered Solutions")
## If uploading Folders at a time for study- use the drag and drop method instead of one at a time.
uploadedfiles = st.file_uploader("Upload Source Documents", type=['pdf','txt','md','py','csv','xls','xlsx','docx','doc'], accept_multiple_files=True)    
if uploadedfiles is not None:
    for file in uploadedfiles:
        save_uploadedfile(file)
# Define the retreiver
# load the vectorstore
if "EMBEDDINGS" not in st.session_state:
        EMBEDDINGS = HuggingFaceInstructEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        st.session_state.EMBEDDINGS = EMBEDDINGS
    
if "DB" not in st.session_state:
        DB = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=st.session_state.EMBEDDINGS,
            client_settings=CHROMA_SETTINGS,
        )
        st.session_state.DB = DB

if "RETRIEVER" not in st.session_state:
        RETRIEVER = DB.as_retriever()
        st.session_state.RETRIEVER = RETRIEVER

llm_config = OpenAI(
        api_key="YOUR_API_KEY_HERE", # API key exposed for this example.  Use env file for production setting.  Local LLM's take any input as key.
        base_url="http://localhost:1234/v1",
        timeout=600,
        temperature=0.3, # Adjust from 0.1 - 0.9  --Lower = more to the point, higher = more creative.
        max_tokens=-1,
    )
    
if "LLM" not in st.session_state:
        LLM = llm_config
        st.session_state["LLM"] = LLM

if "QA" not in st.session_state:
        QA = RetrievalQA.from_chain_type(
            llm=LLM,
            chain_type="stuff",
            retriever=RETRIEVER,
            return_source_documents=True,
        )
        st.session_state["QA"] = QA
# Add a button to run a Python file
if st.button("Study Source Docs"):
    delete_db_folder()
    st.success("Absorbing new documents to memory...")
    # Specify the Python file to run
    python_file_path = os.path.join(os.getcwd(), "study.py")
    # Check if the file exists before attempting to run it
    if os.path.exists(python_file_path):
        # Run the Python file using subprocess
        result = subprocess.run(["python", python_file_path], capture_output=True)
        # Check if the execution was successful
        if result.returncode == 0:
            st.success("Documents Absorbed Successfully!")
            st.success("Refreshing Database...")
            os.system("pkill -f 'streamlit run ragforge.py'")
            time.sleep(3)
            subprocess.Popen(["streamlit", "run", "ragforge.py"])
            os._exit(0)
        else:
            st.error("Error studying source docs. Check the console for details.")
            st.code(result.stderr.decode("utf-8"), language="bash")   
# Add a dropdown to list files in the "SOURCE_DOCUMENTS" folder
with st.expander("List Files in SOURCE_DOCUMENTS Folder"):
    source_documents_folder_path = os.path.join(os.getcwd(), "SOURCE_DOCUMENTS")
    # Check if the folder exists
    if os.path.exists(source_documents_folder_path) and os.path.isdir(source_documents_folder_path):
        # List all files in the folder
        files_in_source_documents_folder = os.listdir(source_documents_folder_path)

    for file_name in files_in_source_documents_folder:
        delete_button_key = f"delete_button_{file_name}"

        # Display file name and delete button
        st.write(file_name)
        if st.button(f"Delete {file_name}", key=delete_button_key):
            # Delete the file if the button is pressed
            file_path = os.path.join(source_documents_folder_path, file_name)
            os.remove(file_path)
            st.success(f"File '{file_name}' deleted.")
# Sidebar contents
with st.sidebar:
    st.title("🌞 RAGForge - Rag-Powered Solutions")
    st.markdown(
        """
    ## Steps📖:
    - Upload Document files via 'Browse files'
    - If uploading entire folders at a time- use the Drag and drop method
    - Run 'Study Source Docs' (press the study button)
    - Documents will be absorbed into new Database
    - Prompt the model for a Response
    Enjoy🌞

    ## Tips for hosting app💡:
    - Run Infinite Databases with 1 model by cloning multiple RAGForge directories and changing Server port only.
    - Run Infinite Databases with Multiple Models by changing API port per model and Server port per RAGForge instance.
    - Serve RAGForge to all devices within a local-network. 
    - Enable Port-forwarding for global access from Mobile devices or other Desktops.
    - Enable VPN for secure-tunneling to localhost serving RAGForge.
    - You can also close this Webpage and STILL have the Streamlit Host Server running in the background.
    
    
    ## About
    This app Absorbs documents and generates responses based on the content. built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [Chroma](https://www.trychroma.com/)
    - [RagForge](https://github.com/HeliosPrimeOne/ragforge)

    API Backend
    - [LM-Studio](https://lmstudio.ai/)
 
    """
    )             
    avs.add_vertical_space(1)
    st.write("Made with 🌞 shine by [HeliosPrime](https://github.com/HeliosPrimeOne)")
    st.write("Product of [PrimeLabs](https://discord.gg/zuudwZG2zg)")
    
    # Add a button for force quit
    if st.button("Force Quit"): 
    # Kill the Streamlit process and exit
        pid = os.getpid()
        os.kill(pid, signal.SIGINT)
    st.write ("Ctrl+c to abort in Terminal")
# Add a button for force restart
if st.button("Force Restart"):
    # Kill the Streamlit process, restart, and exit
    os.system("pkill -f 'streamlit run ragforge.py'")
    time.sleep(3)
    subprocess.Popen(["streamlit", "run", "ragforge.py"])
    os._exit(0)
st.markdown("Check side-bar for Tutorial🌞")
#text input box for the user
prompt = st.text_input("Input your prompt or speak into the mic 🎤️ for mobile🌞")
# Prompt Process
if prompt:
    try:
        # Pass prompt to the LLM
        response = st.session_state["QA"](prompt)
        answer, docs = response["result"], response["source_documents"]
        # Respond On-screen.
        st.write(answer)
    except Exception as e:
        # Display an error message if an exception
        st.error(
        """
    3 Possible Errors:
    - API connection error - Start/Restart Your LLM API Server. Confirm api Ports
    - Database has changed, Refresh page to fix.
    - Out of Memory error = Restart your Streamlit Script from the terminal. Ctrl+c to shutdown app.
        """
    )
    # print the exception for debugging purposes
        print(f"Error: {e}")
    #streamlit expander
    with st.expander("Document Similarity Search"):
        # Find the relevant pages
        search = st.session_state.DB.similarity_search_with_score(prompt)
        # Write out the first
        for i, doc in enumerate(search):
            # print(doc)
            st.write(f"Source Document # {i+1} : {doc[0].metadata['source'].split('/')[-1]}")
            st.write(doc[0].page_content)
            st.write("--------------------------------")
# Set the maximum memory usage threshold (in percentage)
max_memory_threshold = 45  # Adjust as needed
while True:
    # Get the current system memory usage
    memory_usage = psutil.virtual_memory().percent

    # Check if memory usage exceeds the threshold
    if memory_usage >= max_memory_threshold:
        # Kill the Streamlit process, restart, and exit
        os.system("pkill -f 'streamlit run ragforge.py'")
        time.sleep(3)
        subprocess.Popen(["streamlit", "run", "ragforge.py"])
        os._exit(0)
    # Sleep for a short interval before checking again
    time.sleep(60)  # Check every 60 seconds (adjust as needed)