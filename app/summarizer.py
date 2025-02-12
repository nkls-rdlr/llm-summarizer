from langchain_ollama import ChatOllama
import os
from prompts import format_prompt, summarize_prompt
import re
import shutil
import tempfile
import whisper
import yt_dlp


llm = ChatOllama(model="llama3.1:8b", temperature=0.8, num_predict=-1)


def download_audio(url: str) -> str:
    """
    Given a YouTube URL, downloads the audio as .m4a to a temporary directory
    and returns the file path.
    """
    temp_dir = tempfile.mkdtemp()

    opts = {
        "format": "m4a/bestaudio/best",
        "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
            }
        ],
    }

    try:
        with yt_dlp.YoutubeDL(opts, url) as extractor:
            info_dict = extractor.extract_info(url)

        return extractor.prepare_filename(info_dict)

    except Exception as e:
        raise RuntimeError(
            f"An unexpected error occurred during download: {str(e)}"
        )


def download_subtitles(url: str) -> str:
    """
    Given a YouTube URL, downloads the subtitles and returns them as a string
    object.
    """
    temp_dir = tempfile.mkdtemp()

    opts = {
        "writeautomaticsub": True,
        "subtitlesformat": "vtt",
        "skip_download": True,
        "outtmpl": os.path.join(temp_dir, "subs"),
    }

    try:
        with yt_dlp.YoutubeDL(opts) as extractor:
            extractor.download(url)

        with open(os.path.join(temp_dir, "subs.en-US.vtt"), "r") as file:
            subtitles = file.read()

        formatted_subtitles = " ".join(
            re.sub(
                r"\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}",
                "",
                subtitles,
            )
            .replace("&nbsp;", "")
            .split()
        )

        shutil.rmtree(temp_dir)
        return formatted_subtitles

    except Exception as e:
        raise RuntimeError(
            f"An unexpected error occurred during subtitle download: {str(e)}"
        )


def transcribe_audio(file_path: str, model_name: str = "small") -> str:
    """
    Transcribes the audio to text using OpenAI Whisper and cleans up the audio
    file.
    """
    if file_path is not None:
        try:
            model = whisper.load_model(model_name)
            result = model.transcribe(file_path, fp16=False)
            return result["text"]
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred during transcription: {str(e)}"
            )
        finally:
            shutil.rmtree(os.path.dirname(file_path))

    else:
        raise ValueError(
            "There is no audio file under the specified path to transcribe."
        )


def format_transcript(transcript: str) -> str:
    """
    Given a transcript, prompts Llama 3.1 (8B) to format it, adding newlines
    and grouping related sentences into paragraphs. Returns the formatted
    transcript as a Markdown-formatted string.
    """
    formatting_prompt = format_prompt + transcript
    response = llm.invoke(formatting_prompt)

    return response.content


def summarize_transcript(transcript: str) -> str:
    """
    Given a transcript, prompts Llama 3.1 (8B) to create a summary. Returns the
    summary as a Markdown-formatted string.
    """
    summarization_prompt = summarize_prompt + transcript
    response = llm.invoke(summarization_prompt)
    
    return response.content


def generate_summary(url: str) -> str:
    """
    Handler function that takes a YouTube URL as input, transcribes the audio
    and returns a summary of the content as a Markdown-formatted string.
    """
    file_path = download_audio(url)
    transcript = transcribe_audio(file_path)
    return summarize_transcript(transcript)
