# RAGForge: Crafting RAG-powered Solutions for Secure, Local Conversations with Your Documents 🌐 Product of PrimeLabs 🌟

**RAGForge** - RAG `Retrieval-Augmented Generation` (document retrieval) is an open-source endeavor empowering you to engage with your documents while safeguarding your privacy. By operating entirely on your local machine, rest assured that no data ventures beyond your computer. Immerse yourself in the realm of secure, locally-driven document interactions with RAGForge.

## Discord 🌟
- **Come Chat with us on Discord!**: [Click here to join our Discord Server](http://discord.gg/zuudwZG2zg)

## Features 🌟
- **Absolute Confidentiality**: Safeguard your data exclusively on your device, guaranteeing unparalleled security. Load LLM locally through LM-Studio (for simplicity) or alternative methods.
- **Adaptable Model Compatibility**: Effortlessly incorporate a diverse array of open-source models through API integration.
- **Varied Embedding Options**: Select from a spectrum of open-source embeddings for enhanced diversity.
- **Effortless LLM Reuse**: Once acquired, effortlessly utilize your LLM without the necessity for repetitive downloads.

## Coming Soon --
- **Graphical Interface**: Gui connecting directly to API for RAG Solutions.
- **API**: API that you can use for building RAG Applications. LLM within an LLM
- **Chat History**: Remembers your previous conversations (in a session).
- **Whisper feature**: Talk to your Ai's.
- **Migration into PrimeAgents**: To be eventually added into the PrimeAgents Collection.


## Technical Details 🛠️
By choosing appropriate local models and harnessing the capabilities of LangChain, you can execute the complete RAG pipeline on your local setup. No data departs from your environment, ensuring utmost privacy, all while maintaining reasonable performance.

- `study.py` uses `LangChain` tools to parse the document and create embeddings locally using `InstructorEmbeddings`. It then stores the result in a local vector database using `Chroma` vector store.
- `run.py` uses a local LLM to understand questions and create answers. The context for the answers is extracted from the local vector store using a similarity search to locate the right piece of context from the docs.
- You can replace this local LLM with any other LLM you wish to load via API.


## Built Using 🧩
- [LangChain](https://github.com/hwchase17/langchain)
- [InstructorEmbeddings](https://instructor-embedding.github.io/)
- [LLAMACPP](https://github.com/abetlen/llama-cpp-python)
- [ChromaDB](https://www.trychroma.com/)

## Default Local LLM API host - Any local or hosted API service will work.
- [LM-Studio](https://lmstudio.ai/)

## Pre-Reqs : For both LM-Studio & RAGForge
- **ubuntu 22.04** - Preferred - Less bugs - LM-Studio should work right out the box (appImage format).
- **windows 10** - LLM setup Support in LM-Studio Discord or default LLM API service discord.
- **MAC OS 13.6** - LM-Studio only Supports - M1/M2/M3 based Macbooks. NON-intel. Running MacOS 13.6 or newer is required. 
- **VScode** - Optional (preferred).

# Environment Setup 🌍 Terminal or VScode (preferred)

1. 📥 Clone the repo using git:

```shell
git clone https://github.com/HeliosPrimeOne/ragforge.git
```

2. 🐍 Install [conda](https://www.anaconda.com/download) for virtual environment management. Create and activate a new virtual environment.

```shell
conda create -n rag python=3.10.0
```
```shell
conda activate rag
```

3. 🛠️ Install the dependencies using pip

To set up your environment to run the code, navigate to Dir then install all requirements:

```shell
pip install -r requirements.txt
```
**Some systems require torch to be installed manually from here**
- [PyTorch Manual install](https://pytorch.org/get-started/locally/)

## Test dataset

For testing, this repo comes preloaded with [The Art of War by Sun Tzu](https://www.globalgreyebooks.com/art-of-war-ebook.html#downloads) inside `SOURCE_DOCUMENTS` as an example file to use.

## Ingesting your OWN Data.
Put your files in the `SOURCE_DOCUMENTS` folder. You can put multiple folders/files within the `SOURCE_DOCUMENTS` folder and the code will recursively read your files.

### Support file formats:
RAGForge currently supports the following file formats. RAGForge uses `LangChain` for loading these file formats. The code in `constants.py` uses a `DOCUMENT_MAP` dictionary to map a file format to the corresponding loader. In order to add support for another file format, simply add this dictionary with the file format and the corresponding loader from [LangChain](https://python.langchain.com/docs/modules/data_connection/document_loaders/).

```shell
DOCUMENT_MAP = {
    ".txt": TextLoader,
    ".md": TextLoader,
    ".py": TextLoader,
    ".pdf": UnstructuredFileLoader,
    ".csv": CSVLoader,
    ".xls": UnstructuredExcelLoader,
    ".xlsx": UnstructuredExcelLoader,
    ".docx": Docx2txtLoader,
    ".doc": Docx2txtLoader,
}
```

### Start the Study Process

Run the following command to Study all the data.

```shell
python study.py
```

If you have `cuda` Nvidia GPU - your system will default to your GPU for faster processing.


Use the device type argument to specify a given device.
To run on `cpu`

```sh
python study.py --device_type cpu
```

To run on `M1/M2/M3`

```sh
python study.py --device_type mps
```

Use help for a full list of supported devices.

```sh
python study.py --help
```

This will create a new folder called `DB` and use it for the newly created vector store. You can study as many documents as you want, and all will be accumulated in the local embeddings database.
If you want to start from an empty database, delete the `DB` folder and re-study your documents.

**Note**: When you run this for the first time, it will need internet access to download the embedding model (default: `Instructor Embedding`). In the subsequent runs, no data will leave your local environment and you can study data with your local LLM without internet connection.

When DB is created successfully you will see these 2 entries at the end of the study.py process:
- **load INSTRUCTOR_Transformer**
- **max_seq_length  512**

DB creation is complete!


***Note:*** 
- **LM-Studio Quick Setup!**
When you run LM-Studio for the first time, it will need internet connection to download the LLM of your choosing.
- **Search Tab within LM-Studio**: `TheBloke/Mistral-7B-Instruct-v0.2-GGUF`.
- **Download**: `mistral-7b-instruct-v0.2.Q4_K_M.gguf` version.

- **This is a base model version for hardware demand.**

Click on 'local server' tab on LM-Studio



**There are settings in LM-Studio server tab that allow**:
- `Presets`: Use mistral or Zephyr to start - make custom later.
- `Context Length`: (keep it under 4k for Q4 models)
- `GPU loading with layers`: (GPU workload 1-80 --start LOW)
- `CPU loading only`: (max cores -1 OR --avg = 4 cores)
- You will need to adjust according to your hardware.
- Visit the LM-Studio Discord for more info on these settings.

- **Choose Model from Drop-down Menu**
- **Choose server port or leave default 1234**
- **Confirm same port number on** `run.py`
- **Start the Server**


After that you can turn off your internet connection, and the script inference would still work. No data gets out of your local environment.


## Ask questions to your documents, locally!

In order to chat with your documents, run the following command.

```shell
python run.py
```

This will load the DB folder vector store and embedding model. You will be presented with a prompt:

```shell
> Enter a query:
```

After typing your question, hit enter. RAGForge will take some time to reply based on your hardware. Once you hit enter - You can view the server side of LM-Studio to view/confirm streaming of LLM to server console log as well as terminal if ran from CLI (verbose) - then eventually routing into the terminal (or vscode) of RAGForge for the user to view automatically.

Once the answer is generated, you can then ask another question without re-running the script, just wait for the prompt again. --Chat history is in beta may not work for now.
Ctrl+C to abort/exit.




### Extra Options with run.py

You can use the `--show_sources` flag with `run.py` to show which chunks were retrieved by the embedding model. By default, it will show 4 different sources/chunks. You can change the number of sources/chunks accordingly.

```shell
python run.py --show_sources
```


You can use the `--save_qa` flag with `run.py` to save Q&A pairs to a CSV file (Default is False). A folder called qa_history will be created to store QA as a csv file.  Not to be confused with chat history "ChatMemory".

```shell
python run.py --save_qa
```


**BETA**
Another option is to enable chat history. ***Note***: This is disabled by default and can be enabled by using the  `--use_history` flag. The context window is limited so keep in mind enabling history will use it and might overflow.  **Still in BETA**

```shell
python run.py --use_history
```


# How to select different LLM models?

**GGUF FORMAT ONLY**

1. Load LM-Studio and pick a model from the drop-down menu.

# GPU and VRAM Requirements

Below is the VRAM requirement for different models depending on their size (Billions of parameters). The estimates in the table **does not include VRAM used by the Embedding models** - which use an additional 2GB-7GB of VRAM depending on the model.

| Mode Size (B) | float32   | float16   | GPTQ 8bit      | GPTQ 4bit          |
| ------- | --------- | --------- | -------------- | ------------------ |
| 7B      | 28 GB     | 14 GB     | 7 GB - 9 GB    | 3.5 GB - 5 GB      |
| 13B     | 52 GB     | 26 GB     | 13 GB - 15 GB  | 6.5 GB - 8 GB      |
| 32B     | 130 GB    | 65 GB     | 32.5 GB - 35 GB| 16.25 GB - 19 GB   |
| 65B     | 260.8 GB  | 130.4 GB  | 65.2 GB - 67 GB| 32.6 GB - 35 GB    |


# System Requirements

## Python Version

To use this software, you must have Python 3.10 or later installed. Earlier versions of Python will not compile.

### NVIDIA Driver's Issues:

Follow this [page](https://linuxconfig.org/how-to-install-the-nvidia-drivers-on-ubuntu-22-04) to install NVIDIA Drivers.


# Disclaimer

This is a test project to validate the MVP of a fully local solution for question answering using LLMs and Vector embeddings. 
API_KEY is PURELY visible in the code for this example (for simplicity). Local LLM's use any info for api_key. Doesnt have to be real.
Next version will be corrected.
Rec using env file for keys.
Always updating, code can break at anytime. DYOR

-PrimeLabs
