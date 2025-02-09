# llm-summarizer
A simple Streamlit application for transcribing and summarizing YouTube videos.

## Basic functionality
1. User inputs a the URL of a YouTube video in the Streamlit UI.
2. Audio is downloaded (using yt-dlp) to temporary storage, and transcribed using OpenAI Whisper.
3. This transcript, along with a summarization prompt is fed into Llama 3.1 (8B), served using Ollama, which creates a summary of the content.
4. This summary is displayed on the UI.

## Todo and future improvements
- Write Streamlit app
- Dockerize Ollama and Streamlit app
- Allow user to download the summary as PDF
- Allow user to specify whether they want to download full transcript as well
- Allow user to specify custom prompt

### Notes for Dockerization:
- In Streamlit App Container: install ffmpeg and llvm@16
- In Ollama Container: Equivalent of "brew services start ollama"

## Running the project

### Requirements
- Python 3.12
- Poetry
- Docker Desktop
- docker-compose

### Quickstart
- Run "make start" to spin up the containers and access the UI by entering localhost:PORT in your browser.
- To create the Poetry virtual env in the project folder, run: poetry config `virtualenvs.in-project true`.

