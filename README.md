# RAGForge: Crafting RAG-powered Solutions for Secure, Local Conversations with Your Documents 🌐 Product of PrimeLabs 🌞

**RAGForge** - RAG `Retrieval-Augmented Generation` (document retrieval) is an open-source endeavor empowering you to engage with your documents while safeguarding your privacy. By operating entirely on your local machine, rest assured that no data ventures beyond your computer. Immerse yourself in the realm of secure, locally-driven document interactions with RAGForge.

## Discord 🌞
- **Come Chat with us on Discord!**: [Click here to join our Discord Server](http://discord.gg/zuudwZG2zg)

## Features 🌞
- **Graphical Interface**: WEB GUI connecting directly to Model API for RAG Solutions.
- **Absolute Confidentiality**: Safeguard your data exclusively on your device, guaranteeing unparalleled security. Load LLM locally through LM-Studio (for simplicity) or alternative methods.
- **Adaptable Model Compatibility**: Effortlessly incorporate a diverse array of open-source models through API integration.
- **Varied Embedding Options**: Select from a spectrum of open-source embeddings for enhanced diversity.
- **Effortless LLM Reuse**: Once acquired, effortlessly utilize your LLM without the necessity for repetitive downloads.

## Coming Soon --
- **Authentication**: Secure your RAGForge GUI WebUI app with a username and password.(soon soon)
- **Chat History**: Remembers your previous conversations (in a session).
- **Whisper feature**: Talk to your Ai's and have them talk back.
- **Migration into PrimeAgents**: To be eventually added into the PrimeAgents Collection.

## Quick Start
- Create conda env
- Locate directory
- Install Requirements
- Copy files to Source_documents folders
- Start LM-Studio choose your Ai model and start the API server
- CLI Version:  Run `python study.py` For DB creation - Then run `python run.py`
- GUI Version: Run `streamlit run ragforge.py` UI connection info should load in terminal and you can now connect devices to your local or network host URL:

### GUI Connect Options:
**You can now view your Streamlit app in your browser.**

`Local URL: http://localhost:8501`
`Network URL: http://x.x.x.x:8501`

**Modifying Ports & other configs**
- Navigate to `./streamlit` directory inside of RAGForge main directory
- Locate `config.toml` file for editing default configs for the UI app only.
- Edit Ports and other options or leave as default


## Technical Details 🛠️
By choosing appropriate local models and harnessing the capabilities of LangChain, you can execute the complete RAG pipeline on your local setup. No data departs from your environment, ensuring utmost privacy, all while maintaining reasonable performance.

- `study.py` uses `LangChain` tools to parse the document and create embeddings locally using `InstructorEmbeddings`. It then stores the result in a local vector database using `Chroma` vector store.
- `run.py` uses a local LLM to understand questions and create answers. The context for the answers is extracted from the local vector store using a similarity search to locate the right piece of context from the docs.
- You can replace this local LLM with any other LLM you wish to load via API.

This project was designed using multiple sources of related material.

## Built Using 🧩
- [Streamlit](https://streamlit.io/)
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

# Environment Setup 🌍 Terminal/VScode/GUI (preferred)

1. 📥 Clone the repo using git:

```shell
git clone https://github.com/HeliosPrimeOne/ragforge.git
```

2. 🐍 Install [conda](https://www.anaconda.com/download) for virtual environment management. Create and activate a new virtual environment.

```shell
conda create -n rag python=3.11
```
```shell
conda activate rag
```

3. 🛠️ Install the dependencies using pip

To set up your environment to run the code, navigate to the RAGForge dir then install all requirements:

**Purge Cache before we start with the pip cache cmd**

```shell
pip cache purge
```

**Install Requirements**

```shell
pip install -r requirements.txt
```
**Some systems require torch to be installed manually from here**
- [PyTorch Manual install](https://pytorch.org/get-started/locally/)

## Test dataset

For testing, this repo comes preloaded with [The Art of War by Sun Tzu](https://www.globalgreyebooks.com/art-of-war-ebook.html#downloads) inside `SOURCE_DOCUMENTS` as an example file to use.

## Ingesting your OWN Data

### GUI Version:

Click on Browse files button or use the Drag-&-drop method.

Notice the Drop-down menu after files have been uploaded.

You can also delete each file within the `SOURCE_DOCUMENTS` individually before the next study process begins.


### CLI Version:

Put your files in the `SOURCE_DOCUMENTS` folder and the code will recursively read your files.

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
    ".doc": Docx2txtLoader,}
```

### Start the Study Process

### GUI Version

- Press the `study source docs` button on the GUI to study all the data. 

- For entire folders-use the Drag-&-drop method.

- When the embedding model is finished you will see a confirmation - App will refresh with new the Database.


### CLI Version:

- Run the following command to Study all the data.

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

### CLI Version:

- If you want to start from an empty database, delete the `DB` folder and re-study your documents.

### GUI Version:

- When running the `study source docs` function- The DB gets wiped and recreated each time.

**Note for CLI & GUI setups**
- When you run the Study process for the first time, it will need internet access to download the embedding model (default: `Instructor Embedding`). In the subsequent runs, no data will leave your local environment and you can study data with your local LLM without internet connection. Expect a slight initial delay in GUI version when running the `study source docs` for the first time as it needs to download the selected embedding model to begin.

**Embedding Models**
- There’s a few to choose from in the `constants.py` file.
- They use more memory to load so be aware of the hardware demands.
- Just uncomment/comment the model you want to use. It’ll download it locally.
- Then you can disconnect from the internet again per usual if u want.

When DB is created successfully you will see these 2 entries at the end of the `study source docs` / `study.py` process:

### CLI Version:
- **load INSTRUCTOR_Transformer**
- **max_seq_length  512**

### GUI Version:
- **Documents Absorbed Successfully!**
- **Refreshing Database...**

**DB creation is complete!**


***Note:*** 
- **LM-Studio Quick Setup!**
When you run LM-Studio for the first time, it will need internet connection to download the LLM of your choosing.
- **Search Tab within LM-Studio**: `TheBloke/Mistral-7B-Instruct-v0.2-GGUF`.
- **Download**: `mistral-7b-instruct-v0.2.Q4_K_M.gguf` version.

- **This is a base model version for Basic hardware demand.**

Click on 'local server' tab on LM-Studio



**There are settings in LM-Studio server tab that allow**:
- `Presets`: Use mistral or Zephyr to start - make custom later.
- `Context Length`: (keep it under 4k for Q4 models)
- `GPU loading with layers`: (GPU workload 5-50 layers --start LOW)
- `CPU loading only`: (4 cores)
- You will need to adjust according to your hardware.
- Visit the LM-Studio Discord for more info on these settings.

- **Choose Model from Drop-down Menu**
- **Choose server port or leave default 1234**
- **Confirm same port number on**
- CLI Version: `run.py`
- GUI Version: `ragforge.py`
- **Start the Server**


After that you can turn off your internet connection, and the script inference will still function. 
No data leaves your local environment.


## Ask questions to your documents, locally!

### In order to chat with your documents, run the following command.

### CLI Version:

```shell
python run.py
```

This will load the DB folder vector store and embedding model. You will be presented with a prompt:

```shell
> Enter a query:
```


### GUI Version:

```shell
streamlit run ragforge.py
```
- This will load the Streamlit GUI app, DB folder vector store and embedding model.
- You can now interact with the Rag-powered interface.
- You can now close the Webpage and STILL have the Streamlit Host Server running in the background for your other clients to connect to.

## Prompt Response:

- After typing your question, hit enter. RAGForge will take some time to reply based on your hardware. Once you hit enter - You can view the server side of LM-Studio to view/confirm streaming of LLM to server console log as well as terminal if ran from CLI (verbose) - then eventually routing into the Web GUI or terminal (or vscode) of RAGForge for the user to view automatically.

- Once the answer is generated, you can then ask another question without re-running the script, just wait for the prompt again.

- Ctrl+C to abort/exit.





### Extra Options with `run.py` CLI version:

You can use the `--show_sources` flag with `run.py` to show which chunks were retrieved by the embedding model. By default, it will show 4 different sources/chunks. You can change the number of sources/chunks accordingly.

```shell
python run.py --show_sources
```


You can use the `--save_qa` flag with `run.py` to save Q&A pairs to a CSV file (Default is False). A folder called qa_history will be created to store QA as a csv file.  Not to be confused with chat history "ChatMemory".

```shell
python run.py --save_qa
```


## Tips for GUI app hosting💡:
- Run Infinite Databases with 1 model by cloning multiple RAGForge directories and changing Server port only.
- Run Infinite Databases with Multiple Models by changing API port per model and Server port per RAGForge instance.
- Serve RAGForge to all devices within a local-network. 
- Enable Port-forwarding for global access from Mobile devices or other Desktops.
- Enable VPN for secure-tunneling to localhost serving RAGForge.
- You can also close this Webpage and STILL have the Streamlit Host Server running in the background.


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

Follow this [page](https://linuxconfig.org/how-to-install-the-nvidia-drivers-on-ubuntu-22-04) to install NVIDIA Drivers for linux.

### Work-arounds for Web GUI:
- Memory (RAM) has been capped at 45% to Prevent Server Unstableness. If you constantly run above 45% - change the Cap setting in the Ragforge.py Coding.
- If Force Quit from GUI or Ctrl+c from terminal doesn't stop script - use task manager/system monitor to Kill script.
- If Receving a local Port error from terminal `Port xxxx is already in use` - use task manager/system monitor to Kill script and restart GUI.


# Disclaimer

This is a test project to validate the MVP of a fully local solution for question answering using LLMs and Vector embeddings. 
API_KEY is PURELY visible in the code for this example (for simplicity). Local LLM's use any info for api_key. Doesnt have to be real.
Use .env file for a production setting.
Rec using env file for keys.
Always updating, code can break at anytime. DYOR

-PrimeLabs
