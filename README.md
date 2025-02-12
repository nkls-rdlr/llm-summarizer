# llm-summarizer
A simple LLM application for summarizing the content of YouTube videos that runs entirely locally, powered by Streamlit. No external API calls are made, so it's entirely free to use.

## Basic functionality
1. User inputs the URL of a YouTube video in the UI, and selects whether they want to use subtitles or an AI-generated transcript.
2. Audio or subtitles are downloaded to temporary storage using yt-dlp, and, if selected by the user, transcribed using OpenAI Whisper.
3. The transcript, along with a summarization prompt, is then fed into Llama 3.1 (8B model served with Ollama), which creates a summary of the content. There is also a second request to format the transcript, which is run asynchronously.
4. The summary is displayed on the UI, with an option to download both the summary as well as the transcript used to generate it in PDF format.

## Todo and future improvements
- Move function calls into client.py so we can generate a spinner for each part (Downloading audio/transcript.../Transcribing audio.../Creating summary...)
- Option to download full transcript (above will enable this)
- Option to download and use the Youtube-generated subtitles instead of the transcription service (Above will enable this)
- Dockerize project (Ollama + Streamlit)
(- Allow user to specify custom prompt)
(- Allow user to upload transcript to summarize)
(- More customization options)

## Limitations
Particularly the transcription part is, at least on Apple Silicon, rather slow, as there are currently some compatibility issues with running OpenAI Whisper on Apple GPUs (see e.g. [here](https://github.com/pytorch/pytorch/issues/129842)). Besides, there seems to be little to no possibility to use Apple GPUs when running the application via Docker (see e.g. [here](https://chariotsolutions.com/blog/post/apple-silicon-gpus-docker-and-ollama-pick-two/)), which I am planning to eventually do in order to make it more portable.

To state the obvious, if this was an actual service for end users, it should be run on Nvidia GPUs to speed up inference.

### Notes for Dockerization:
- In Streamlit App Container: install ffmpeg and llvm@16
- In Ollama Container: Equivalent of "brew services start ollama"

## Running the project

### Requirements
- Python 3.12
- Poetry (`pip install poetry`)
- Docker Desktop
- docker-compose

- (Currently: ffmpeg, llvm@16)


### Quickstart
- To ensure the Poetry virtual environment is created in the project folder, run: `poetry config virtualenvs.in-project true`.
- Once initialized, the virtual environment can be activated by running `make env` or `source .venv/bin/activate`.
- Make sure all dependencies are installed by running `poetry install`.
- Run `make st` or `streamlit run app/client.py` from the root directory of the project to start up Streamlit. If it doesn't open automatically, access the UI by entering `localhost:8501` in your browser.

- (Run `make start` to spin up the containers and access the UI by entering `localhost:8501` in your browser.)
