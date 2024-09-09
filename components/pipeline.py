from haystack import Document, Pipeline
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.query_checker import QueryChecker
from components.query_processor import QueryProcessor
from components.report_generator import ReportGenerator
from haystack.components.converters import OutputAdapter


class pipeline:

    query_processor = QueryProcessor()
    query_checker = QueryChecker()
    report_generator = ReportGenerator()
    query_pipeline = Pipeline()
    query_pipeline.add_component("query_processor", query_processor)
    query_pipeline.add_component("query_checker", query_checker)
    query_pipeline.add_component("report_generator", report_generator)
    query_pipeline.connect(
        sender="query_processor.db_output", receiver="query_checker.report"
    )
    query_pipeline.connect(
        sender="query_checker.suggestion", receiver="query_processor.natural_language"
    )

    def query_run(self, natural_language: str):
        result = self.query_pipeline.run({"query_processor.natural_language": natural_language})
        return result


if name == "__main__":
    pipeline = pipeline()
    pipeline.draw(path="pipeline.png")
    #print(
    #    pipeline.query_run(
    #        "I want the names of all employees that have minimum salary of 199999 and order them by their city name."
    #    )
    #)
