"""
NOTE: THESE TESTS NEED UPDATING. PLEASE DO NOT USE THEM AS A REFERENCE.
See the README for more information on how to use the project.
Feel free to make a PR to update these tests.
"""


import unittest
from unittest.mock import patch
from hypothesis.generator import generate_new_hypothesis

class TestHypothesisGenerator(unittest.TestCase):

    @patch('hypothesis.generator.call_openai')
    def test_generate_new_hypothesis_output_type(self, mock_call_openai):
        # Mocking the call_openai function
        mock_call_openai.return_value = '{"content": "Mocked hypothesis based on input data"}'

        # Test if generate_new_hypothesis returns a string
        result = generate_new_hypothesis("test query", [], [])
        self.assertIsInstance(result, str)

    @patch('hypothesis.generator.call_openai')
    def test_generate_new_hypothesis_non_trivial_output(self, mock_call_openai):
        # Mocking the call_openai function
        mock_call_openai.return_value = '{"content": "Mocked hypothesis based on input data"}'

        # Test if generate_new_hypothesis output is non-trivial
        result = generate_new_hypothesis("test query", [], [])
        self.assertTrue(len(result) > 0 and result != "test query")

if __name__ == "__main__":
    unittest.main()
