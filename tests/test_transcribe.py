from app.summarizer import transcribe_audio
import os
import pytest
import tempfile


def test_file_path_does_not_exist():
    """
    This test asserts that the transcribe_audio() function throws a 
    FileNotFoundError if it is passed a file path that doesn't exist.
    """
    non_existent_file_path = "non/existent/file/path.m4a"

    with pytest.raises(FileNotFoundError):
        transcribe_audio(non_existent_file_path)


def test_no_file_in_filepath():
    """
    This test asserts that the transcribe_audio() function throws a 
    FileNotFoundError if it is a file path that doesn't contain anything.
    """
    empty_file_path = tempfile.mkdtemp()

    with pytest.raises(FileNotFoundError):
        transcribe_audio(empty_file_path)

    os.rmdir(empty_file_path)


def test_transcript_not_empty():
    """
    This test asserts that the transcribe_audio() function returns a non-empty
    result when passed an audio file. This audio has been taken from 
    https://tinyurl.com/kaggleaudio (sample audio data).
    """
    file_path = "tests/sample_audio.wav"
    transcript = transcribe_audio(file_path=file_path, remove_tree=False)

    assert transcript
