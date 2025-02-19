from langchain_ollama import ChatOllama
import os
from app.prompts import format_prompt, summarize_prompt
import re
import shutil
import tempfile
import whisper
import yt_dlp


class YouTubeSummarizer:

    def __init__(self):
        """
        Initializes the YouTubeSummarizer class with a ChatOllama LLM.
        """
        self.llm = ChatOllama(
            model="llama3.1:8b", temperature=0.8, num_predict=-1
        )

    @staticmethod
    def download_audio(url: str) -> str:
        """
        Given a YouTube URL, downloads the audio as .m4a to a temporary
        directory and returns the file path.
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

        if not re.match(
            r"https?:\/\/(?:www\.)?(?:youtube\.com\/|youtu\.be\/)[\w-]+", url
        ):
            raise ValueError("Please enter a YouTube URL with a valid format.")

        try:
            with yt_dlp.YoutubeDL(opts, url) as extractor:
                info_dict = extractor.extract_info(url)

            return extractor.prepare_filename(info_dict)

        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred during download: {str(e)}"
            )

    @staticmethod
    def download_subtitles(url: str) -> str:
        """
        Given a YouTube URL, downloads the subtitles and returns them as a
        string object.
        """
        temp_dir = tempfile.mkdtemp()

        opts = {
            "writeautomaticsub": True,
            "subtitlesformat": "vtt",
            "skip_download": True,
            "outtmpl": os.path.join(temp_dir, "subs"),
        }

        if not re.match(
            r"https?:\/\/(?:www\.)?(?:youtube\.com\/|youtu\.be\/)[\w-]+", url
        ):
            raise ValueError("Please enter a YouTube URL with a valid format.")

        try:
            with yt_dlp.YoutubeDL(opts) as extractor:
                extractor.download(url)

            with open(
                os.path.join(
                    temp_dir, "".join(map(str, os.listdir(temp_dir)))
                ),
                "r",
            ) as file:
                subtitles = file.read()

            shutil.rmtree(temp_dir)
            return str(subtitles)

        except Exception as e:
            raise RuntimeError(
                f"""An unexpected error occurred during subtitle download: 
                {str(e)}"""
            )

    @staticmethod
    def format_subtitles(subtitles: str) -> str:
        """
        Given an unformatted subtitles string object, removes timestamps and
        non-breaking spaces, returning a single-line string.
        """
        if not subtitles:
            raise ValueError("There are no valid subtitles to format.")

        try:
            formatted_subtitles = " ".join(
                re.sub(
                    r"\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}",
                    "",
                    subtitles,
                )
                .replace("&nbsp;", "")
                .split()
            )
            return str(formatted_subtitles)
        except Exception as e:
            raise RuntimeError(
                f"""An unexpected error occurred during subtitle formatting: 
                {str(e)}"""
            )

    @staticmethod
    def transcribe_audio(
        file_path: str,
        delete_tempdir: bool = True,
        whisper_model: str = "small",
    ) -> str:
        """
        Transcribes the audio to text using OpenAI Whisper and cleans up the
        audio file.
        """
        if os.path.exists(file_path) and os.path.isfile(file_path):
            try:
                model = whisper.load_model(whisper_model)
                result = model.transcribe(file_path, fp16=False)
                return result["text"]
            except Exception as e:
                raise RuntimeError(
                    f"""
                    An unexpected error occurred during transcription: 
                    {str(e)}"""
                )
            finally:
                if delete_tempdir:
                    shutil.rmtree(os.path.dirname(file_path))
        else:
            raise FileNotFoundError(
                "There is no audio under the specified path to transcribe."
            )

    def format_transcript(self, transcript: str) -> str:
        """
        Given a transcript, prompts Llama 3.1 (8B) to format it, adding
        newlines and grouping related sentences into paragraphs. Returns the
        formatted transcript as a Markdown-formatted string.
        """
        if not transcript:
            raise ValueError("Transcript is empty or does not exist.")

        try:
            formatting_prompt = format_prompt + transcript
            response = self.llm.invoke(formatting_prompt)
            return str(response.content)
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred during transcription: {str(e)}"
            )

    def summarize_transcript(self, transcript: str) -> str:
        """
        Given a transcript, prompts Llama 3.1 (8B) to create a summary. Returns
        the summary as a Markdown-formatted string.
        """
        if not transcript:
            raise ValueError("Transcript is empty or does not exist.")

        try:
            summarization_prompt = summarize_prompt + transcript
            response = self.llm.invoke(summarization_prompt)
            return str(response.content)
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred during transcription: {str(e)}"
            )
