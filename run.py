import os
import time
import logging
import click
import openai
import torch
import utils
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_openai import OpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain_community.vectorstores import Chroma
from constants import (
    EMBEDDING_MODEL_NAME,
    PERSIST_DIRECTORY,
    CHROMA_SETTINGS
)

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])



def load_remote_model(api_key, base_url):
    openai.api_key = api_key
    openai.base_url = base_url

def retrieval_qa_pipeline(device_type, use_history):
    embeddings = HuggingFaceInstructEmbeddings(model_name=EMBEDDING_MODEL_NAME, model_kwargs={"device": device_type})
    db = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings,
        client_settings=CHROMA_SETTINGS
    )
    retriever = db.as_retriever()
    




    llm_config = OpenAI(
        api_key="YOUR_API_KEY_HERE",   # API key exposed for this example.  Use env file for real key.  Local LLM's take any input as key.
        base_url="http://localhost:1234/v1",
        timeout=600,
        temperature=0.3, # Adjust from 0.1 - 0.9  --Lower = more to the point, higher = more creative. Verify which take precedence (script or llm api)
        max_tokens=-1,
    )

    llm = llm_config

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        callbacks=callback_manager,
        
    )

    return qa

@click.command()
@click.option(
    "--device_type",
    default="cuda" if torch.cuda.is_available() else "cpu",
    type=click.Choice([
        "cpu", "cuda", "ipu", "xpu", "mkldnn", "opengl", "opencl", "ideep", "hip", "ve", "fpga", "ort", "xla",
        "lazy", "vulkan", "mps", "meta", "hpu", "mtia",
    ]),
    help="Device to run on. (Default is cuda)",
)
@click.option(
    "--show_sources",
    "-s",
    # default=True,
    is_flag=True,
    help="Show sources along with answers (Default is False)",
)
@click.option(
    "--use_history",
    "-h",
    default=False,
    is_flag=True,
    help="Use history (Default is False)",
)
@click.option(
    "--save_qa",
    is_flag=True,
    help="Whether to save Q&A pairs to a CSV file (Default is False)",
)

def main(device_type, show_sources, use_history, save_qa):
    logging.info(f"Running on: {device_type}")
    logging.info(f"Display Source Documents set to: {show_sources}")
    logging.info(f"Use history set to: {use_history}")

    qa = retrieval_qa_pipeline(device_type, use_history)
    
    while True:
        query = input("\nEnter a query: ")
        if query == "exit":
            break
        res = qa(query)
        answer, docs = res["result"], res["source_documents"]

        print("\n\n> Question:")
        print(query)
        print("\n> Answer:")
        print(answer)



        if show_sources:
            time.sleep(2)

            print("\033[38;2;255;165;0mLoading Sources from response...\033[0m")

            print("----------------------------------SOURCE DOCUMENTS---------------------------")
            for document in docs:
                print("\n> " + document.metadata["source"] + ":")
                print(document.page_content)
            print("----------------------------------SOURCE DOCUMENTS---------------------------")

        if save_qa:
            utils.log_to_csv(query, answer)

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s", level=logging.INFO
    )
    main()
