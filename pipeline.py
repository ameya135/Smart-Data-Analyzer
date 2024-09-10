import os
import sys

from haystack import Pipeline
from haystack.components.routers import ConditionalRouter
from haystack.document_stores.in_memory import InMemoryDocumentStore

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.query_checker import QueryChecker
from components.query_processor import QueryProcessor
from components.report_generator import ReportGenerator

# Define the routes for the ConditionalRouter
routes = [
    {
        "condition": "{{valid is true}}",  # When the query is valid, send it to report_generator
        "output": "{{query}}",  # Pass the query to the next step
        "output_name": "valid_query",
        "output_type": str,
    },
    {
        "condition": "{{valid is none or valid is false}}",  # When invalid, send it back to query_processor
        "output": "{{query}}",  # Pass the query back to the query_processor
        "output_name": "invalid_query",
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
    sender="query_processor.db_output", receiver="query_checker.query"
)
query_pipeline.connect(sender="router.valid_query", receiver="report_generator.query")
query_pipeline.connect(
    sender="router.invalid_query", receiver="query_processor.natural_language"
)

payload = {
    "natural_language": "Sales data from October 2023 to December 2023",
}

kwargs = {"valid": False, "query": payload}
result = router.run(**kwargs)
print(result)
