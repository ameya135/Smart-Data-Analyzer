import os
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main


def test_parse_document_structure():
    text_input = "Tell me about sales from October 2023 to December 2023"

    actual_output = main(text_input)

    assert isinstance(actual_output, dict), "Output is not a dictionary"

    assert "doc_title" in actual_output, "Missing 'doc_title' key"

    for i in range(1, 3):
        header_key = f"header{i}"
        assert header_key in actual_output, f"Missing '{header_key}' key"

        header = actual_output[header_key]
        assert isinstance(header, dict), f"'{header_key}' is not a dictionary"

        assert "img1" in header, f"Missing 'img1' key in '{header_key}'"
        assert "imgDesc1" in header, f"Missing 'imgDesc1' key in '{header_key}'"
        assert "content1" in header, f"Missing 'content1' key in '{header_key}'"
