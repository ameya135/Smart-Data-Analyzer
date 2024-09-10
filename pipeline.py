import os
import sys

from haystack import Pipeline
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.routers import ConditionalRouter
from haystack.document_stores.in_memory import InMemoryDocumentStore

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from haystack.components.converters import OutputAdapter

from components.query_checker import QueryChecker
from components.query_processor import QueryProcessor
from components.report_generator import ReportGenerator

# Router configuration
routes = [
    {
        "condition": "{{valid}}",
        "output": "{{query_checker.response}",
        "output_name": "valid_query",
        "output_type": str,
    },
    {
        "condition": "{{not valid}",
        "output": "{{query_checker.response}}",
        "output_name": "valid_query",
        "output_type": str,
    },
]

router = ConditionalRouter(routes=routes)
query_processor = QueryProcessor()
query_checker = QueryChecker()
report_generator = ReportGenerator()
query_pipeline = Pipeline()
query_pipeline.add_component("router", router)
query_pipeline.add_component("query_processor", query_processor)
query_pipeline.add_component("query_checker", query_checker)
query_pipeline.add_component("report_generator", report_generator)
query_pipeline.connect(
    sender="query_processor.db_output", receiver="query_checker.report"
)
query_pipeline.connect(
    sender="query_checker.suggestion", receiver="query_processor.natural_language"
)


payload = {
    "natural_language": "Sales data from October 2023 to December 2023",
}
print(query_pipeline.run(data=payload))
