# llm-summarizer
A simple Streamlit application for summarizing the content of YouTube videos. Simply start the Streamlit app (make sure Ollama is running), paste the URL of a YouTube video you want to generate a summary for and wait for it to be completed.

## Basic functionality
1. User inputs the URL of a YouTube video in the Streamlit UI.
2. Audio is downloaded to temporary storage using yt-dlp, and transcribed using OpenAI Whisper.
3. The transcript, along with a summarization prompt, is fed into Llama 3.1 (8B model served with Ollama), which creates a summary of the content.
4. This summary is displayed on the UI, and can be downloaded in PDF format.

## Todo and future improvements
- Option to download full transcript
- Option to download and use the Youtube-generated subtitles instead of the transcription service
- Allow user to specify custom prompt
(- Allow user to upload transcript to summarize)
- Dockerize Ollama and Streamlit app
- More customization options

## Limitations
Particularly the transcription part is, at least on Apple Silicon, rather slow, as there are currently some compatibility issues with running OpenAI Whisper on Apple GPUs (see e.g. [here](https://github.com/pytorch/pytorch/issues/129842)). Besides, there seems to be little to no possibility to use Apple GPUs when running the application via Docker (see e.g. [here](https://chariotsolutions.com/blog/post/apple-silicon-gpus-docker-and-ollama-pick-two/)), which I am planning to eventually do in order to make it more portable.

To state the obvious, if this was an actual service for end users, it should be run on a machine with a Nvidia GPU.

### Notes for Dockerization:
- In Streamlit App Container: install ffmpeg and llvm@16
- In Ollama Container: Equivalent of "brew services start ollama"

## Running the project

### Requirements
- Python 3.12
- Poetry
- Docker Desktop
- docker-compose
- (Currently: ffmpeg, llvm@16)


### Quickstart
- To ensure the Poetry virtual environment is created in the project folder, run: `poetry config virtualenvs.in-project true`.
- Once initialized, the virtual environment can be activated by running `make venv` or `source .venv/bin/activate`.
- Run `make streamlit` or `streamlit run app/client.py` from the root directory of the project to start up Streamlit. If it doesn't open automatically, access the UI by entering `localhost:8501` in your browser.
- (Run `make start` to spin up the containers and access the UI by entering `localhost:8501` in your browser.)
