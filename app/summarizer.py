from langchain_ollama import ChatOllama
import os
import tempfile
import shutil
import whisper
import yt_dlp


llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0.8,
    num_predict=-1
)


def _download_audio(url: str) -> str:
    """
    Given a YouTube URL, downloads the audio as .m4a to a temporary directory 
    and returns the file path.
    """
    temp_dir = tempfile.mkdtemp()

    opts = {
    'format': 'm4a/bestaudio/best',
    'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
        }]
    }

    try:
        with yt_dlp.YoutubeDL(opts, url) as extractor:
            info_dict = extractor.extract_info(url)
        return extractor.prepare_filename(info_dict)
    except Exception as e:
        raise RuntimeError(
            f"An unexpected error occurred during download: {str(e)}"
        )


def _transcribe_audio(file_path: str, model_name: str = "medium") -> str:
    """
    Transcribes the audio to text using OpenAI Whisper and cleans up the audio 
    file.
    """
    if file_path is not None:
        try:
            model = whisper.load_model(model_name)
            result = model.transcribe(file_path)
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


def _summarize_transcript(transcript: str) -> str:
    """
    Given a transcript, prompts Llama 3.1  (8B) to create a summary. Returns 
    the summary as a Markdown-formatted string.
    """
    with open('app/prompt.txt', 'r') as file:
        prompt = file.read()

    summarization_prompt = prompt + transcript
    response = llm.invoke(summarization_prompt)
    return response.content


def generate_summary(url: str) -> str:
    """
    Handler function that takes a YouTube URL as input, transcribes the audio 
    and returns a summary of the content as a Markdown-formatted string.
    """
    file_path = _download_audio(url)
    transcript = _transcribe_audio(file_path)
    return _summarize_transcript(transcript)


if __name__ == "__main__":
    summary = generate_summary(url="https://www.youtube.com/watch?v=LPZh9BOjkQs")
    print(summary)
