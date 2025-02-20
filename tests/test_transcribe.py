from app.summarizer import YouTubeSummarizer
import os
import pytest
import tempfile

summarizer = YouTubeSummarizer()


def test_error_if_file_path_does_not_exist():
    """
    This test asserts that the transcribe_audio() function throws a
    FileNotFoundError if it is passed a file path that doesn't exist.
    """
    non_existent_file_path = "non/existent/file/path.m4a"

    with pytest.raises(FileNotFoundError):
        summarizer.transcribe_audio(non_existent_file_path)


def test_error_if_no_file_in_filepath():
    """
    This test asserts that the transcribe_audio() function throws a
    FileNotFoundError if it is a file path that doesn't contain anything.
    """
    empty_file_path = tempfile.mkdtemp()

    with pytest.raises(FileNotFoundError):
        summarizer.transcribe_audio(empty_file_path)

    os.rmdir(empty_file_path)


@pytest.mark.skipif(
    bool(os.getenv("GITHUB_ACTIONS")), reason="Skip during GHA Workflow"
)
def test_transcript_not_empty():
    """
    This test asserts that the transcribe_audio() function returns a non-empty
    string object when passed an audio file. This audio has been taken from
    https://tinyurl.com/kaggleaudio. It has not been pushed to remote as Git
    seems to be having problems with handling large non-text objects.
    """
    file_path = "tests/fixtures/audio.wav"
    transcript = summarizer.transcribe_audio(
        file_path=file_path, delete_tempdir=False
    )

    assert transcript
    assert isinstance(transcript, str)


@pytest.mark.skipif(
    bool(os.getenv("GITHUB_ACTIONS")), reason="Skip during GHA Workflow"
)
def test_error_if_wrong_model_config():
    """
    This test asserts that the transcribe_audio() function throws a
    RuntimeError when passed a correct file_path but false model config.
    """
    file_path = "tests/fixtures/audio.wav"

    with pytest.raises(RuntimeError):
        summarizer.transcribe_audio(
            file_path=file_path,
            whisper_model="invalid_value",
            delete_tempdir=False,
        )
