# llm-summarizer
A simple LLM application for summarizing the content of YouTube videos that runs locally, powered by Streamlit and Ollama. Enter a YouTube URL, pick a transcription option, and wait for your LLM-generated summary to be generated.

## Basic functionality
1. User inputs the URL of a YouTube video in the UI, and selects whether they want to use subtitles or an AI-generated transcript as a basis for the summary.
2. Audio (or subtitles) is downloaded to temporary storage using yt-dlp, and, if audio, transcribed using OpenAI Whisper.
3. The transcript (or subtitles), along with a summarization prompt, is then fed into Llama 3.1 (8B model served with Ollama), which creates a summary of the content. There is also a second request to format the transcript, which is run asynchronously.
4. The summary is displayed on the UI, with an option to download the summary, or the transcript used to generate it in PDF format (unfortunately it's not possible to click both buttons in a single Streamlit session).

## Possible future improvements
- Make the app stateful, so users can interact with multiple components without refreshing the page
- Allow user to specify custom prompt
- Allow user to upload transcript to summarize

## Limitations

### State

Streamlit is by design a stateless framework, meaning that it "reruns your script from top to bottom every time you interact with your app" (see [here](https://docs.streamlit.io/develop/concepts/architecture/session-state)). This makes sense when reloading the page or entering a new URL, but less so when you click one of the download buttons, as it refreshes the page. While there are workarounds, this was beyond the scope of this project.

If this app was to be served to end users, a framework would need to be selected that preserves state after clicking a button (so that end users can download both the transcript and the summary individually).

### Performance
Particularly the transcription part is, at least on Apple Silicon, rather slow, as there are currently some compatibility issues with running OpenAI Whisper on Apple GPUs (see e.g. [here](https://github.com/pytorch/pytorch/issues/129842)). Ollama does locally run on Apple Silicon GPU, but this is not possible when running Ollama via Docker (see e.g. [here](https://ollama.com/blog/ollama-is-now-available-as-an-official-docker-image)), which is why I ultimately opted not to Dockerize the project.

To state the obvious, if this was an actual service for end users, it should be run on Nvidia GPUs (and ideally Linux) to speed up inference.

## Running the project

### Requirements
- Python 3.12 (`brew install python@3.12`)
- ffmpeg (`brew install ffmpeg`)
- LLVM 16 (`brew install llvm@16`)
- hdf5 (`brew install hdf5`)
- Poetry (`pip install poetry`)

### Quickstart
- To ensure the Poetry virtual environment is created in the project folder, run: `poetry config virtualenvs.in-project true`.
- Once initialized, the virtual environment can be activated by running `make env` or `source .venv/bin/activate`.
- Make sure all dependencies are installed by running `poetry install`.
- Run `make st` or `streamlit run app/client.py` from the root directory of the project to start up Streamlit. The UI should open automatically on `localhost:8501`.
