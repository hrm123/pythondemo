from pprint import pprint
import unittest
from unittest.mock import patch
import ytbot_local_ as ytbot_local_alt
from ytbot_local_ import get_video_id, get_transcript, process, chunk_transcript, summarize_video, answer_question


class TestSummarizeVideo(unittest.TestCase):
    def test_summarize_video(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        summary = summarize_video(url)
        pprint(summary)
        self.assertIsNotNone(summary)


class TestGetVideoId(unittest.TestCase):
    def test_get_video_id(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.assertEqual(get_video_id(url), "dQw4w9WgXcQ")


class TestGetTranscript(unittest.TestCase):
    def test_get_transcript(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        transcript = get_transcript(url)
        print(transcript)
        self.assertIsNotNone(transcript)


class TestProcess(unittest.TestCase):
    def test_process(self):
        processed_transcript = [
            {"text": "Hello, world!", "start": 0.0, "duration": 2.0},
            {"text": "This is a test.", "start": 2.0, "duration": 3.0}
        ]
        expected_output = "Text: Hello, world! Start: 0.0\nText: This is a test. Start: 2.0\n"
        actual = process(processed_transcript)
        self.assertEqual(actual, expected_output)

    def test_process_another(self):
        processed_transcript = """Text: We're no strangers to love. Start: 0.0
            Text: You know the rules and so do I. Start: 3.5
            Text: A full commitment's what I'm thinking of. Start: 7.5"""
        resp = process(processed_transcript)
        print(resp)


class TestChunks(unittest.TestCase):
    def test_chunks_other(self):
        processed_transcript = """Text: We're no strangers to love. Start: 0.0
            Text: You know the rules and so do I. Start: 3.5
            Text: A full commitment's what I'm thinking of. Start: 7.5"""
        expected_output = [
            "Text: We're no strangers to love. Start: 0.0\nText: You know the rules and so do I. Start: 3.5",
            "Text: A full commitment's what I'm thinking of. Start: 7.5"
        ]
        actual = chunk_transcript(processed_transcript)
        pprint(expected_output)
        pprint(actual)
        self.assertEqual(actual, expected_output)


class TestFallbackBehavior(unittest.TestCase):
    def test_summarize_video_falls_back_without_watsonx_credentials(self):
        with patch.object(ytbot_local_alt, "setup_credentials", side_effect=Exception("missing credentials")):
            result = ytbot_local_alt.summarize_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.assertIn("Unable to summarize", result)


if __name__ == '__main__':
    unittest.main()
