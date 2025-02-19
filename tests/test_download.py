from app.summarizer import YouTubeSummarizer
import pytest
import re

summarizer = YouTubeSummarizer()


def test_error_if_url_is_invalid_audio():
    """
    This test asserts that the download_audio() function throws a ValueError
    when passed an invalid URL.
    """
    invalid_url = "youtuuuuube.com/invalidurl"

    with pytest.raises(ValueError):
        summarizer.download_audio(invalid_url)


def test_error_if_url_is_invalid_subtitles():
    """
    This test asserts that the download_subtitles() function throws a
    ValueError when passed an invalid URL.
    """
    invalid_url = "youtuuuuube.com/invalidurl"

    with pytest.raises(ValueError):
        summarizer.download_subtitles(invalid_url)


def test_format_subtitles_returns_non_empty_string_object():
    """
    This test asserts that the format_subtitles() function returns a non-empty
    string object when passed a valid string as input.
    """
    with open("tests/fixtures/sample_subtitles.vtt", "r") as file:
        subtitles = file.read()

    formatted_subtitles = summarizer.format_subtitles(subtitles)

    assert formatted_subtitles
    assert isinstance(formatted_subtitles, str)


def test_format_subtitles_returns_string_with_no_timestamps_or_nbsp():
    """
    This test asserts that the format_subtitles() function returns a string
    object that does not contain timestamps or non-breaking spaces.
    """
    with open("tests/fixtures/sample_subtitles.vtt", "r") as file:
        subtitles = file.read()

    formatted_subtitles = summarizer.format_subtitles(subtitles)

    assert not re.search(
        r"\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}",
        formatted_subtitles,
    )
    assert not re.search("&nbsp;", formatted_subtitles)
