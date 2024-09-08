import os
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.query_checker import QueryChecker
from components.query_processor import QueryProcessor


def test_query_processor():
    query_processor = QueryProcessor()
    result = query_processor.run(
        "Tell me about Sales from December 2020 to January 2021"
    )
    assert isinstance(result, dict), "Output is not a dictionary"
    assert "sql_query" in result, "Missing 'sql_query' key"
    assert "data" in result, "Missing 'data' key"
    assert "user_query" in result, "Missing 'user_query' key"


def test_query_checker():
    query_checker = QueryChecker()
    query_checker_input = {
        "user_query": "Tell me about Sales from December 2020 to January 2021",
        "sql_query": "SELECT * FROM sales WHERE date BETWEEN '2020-12-01' AND '2021-01-31'",
        "data": {"sales": "data"},
    }
    result = query_checker.run(query_checker_input)
    assert isinstance(result, dict), "Output is not a dictionary"
    assert "user_query" in result, "Missing 'user_query' key"
    assert "sql_query" in result, "Missing 'sql_query' key"
    assert "data" in result, "Missing 'data' key"
    assert "valid" in result, "Missing 'valid' key"
