from haystack import Document, Pipeline
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components import query_processor, query_checker
from haystack.components.converters import OutputAdapter

class pipeline:
    
    adaptor = OutputAdapter()
    query_processor = QueryProcessor()
    query_checker = QueryChecker()

    query_pipeline = Pipeline()
    query_pipeline.add_component("query_processor", query_processor)
    query_pipeline.add_component("query_checker", query_checker)
    query_pipeline.connect(sender="query_processor.report", receiver="query_checker.report")
    query_pipeline.connect(sender="query_checker.suggestion", receiver="query_processor.query")

    def query_run(self, query):
        result = self.query_pipeline.run({"query_processor": {"query": query}})
        return result

if name == "__main__":
    pipeline = pipeline()
    print(pipeline.query_run("I want the names of all employees that have minimum salary of 199999 and order them by their city name."))

