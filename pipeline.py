import os
import sys
from os import PathLike

from haystack import Pipeline
from haystack.components.routers import ConditionalRouter
from haystack.core.pipeline.template import Path
from haystack.document_stores.in_memory import InMemoryDocumentStore

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.query_checker import QueryChecker
from components.query_processor import QueryProcessor
from components.report_generator import ReportGenerator

# Define the routes for the ConditionalRouter
routes = [
    {
        "condition": "{{valid is true}}",  # When the query is valid, send it to report_generator
        "output": "{{db_query}}",  # Pass the query to the report_generator
        "output_name": "valid_query",
        "output_type": str,
    },
    {
        "condition": "{{valid is none or valid is false}}",  # When invalid, send it back to query_processor
        "output": "{{db_query}}",  # Pass the query back to the query_processor
        "output_name": "invalid_query",
        "output_type": str,
    },
]

# Create components
router = ConditionalRouter(routes=routes)
query_processor = QueryProcessor()
query_checker = QueryChecker()
report_generator = ReportGenerator()

# Create the pipeline
query_pipeline = Pipeline()

# Add components to the pipeline
query_pipeline.add_component("query_processor", query_processor)
query_pipeline.add_component("query_checker", query_checker)
query_pipeline.add_component("report_generator", report_generator)
query_pipeline.add_component("router", router)

# Connect components
query_pipeline.connect(
    sender="query_processor.db_output", receiver="query_checker.db_output"
)
query_pipeline.connect(sender="query_processor.db_query", receiver="query_checker.db_query")
query_pipeline.connect(
    sender="query_processor.natural_language", receiver="query_checker.natural_language"
)
query_pipeline.connect("router.valid_query", "report_generator.db_output")
query_pipeline.connect("router.invalid_query", "query_processor.db_query")
query_pipeline.connect(sender="query_checker.valid", receiver="router")
query_pipeline.connect(
    sender="router.invalid_query", receiver="query_processor.natural_language"
)
query_pipeline.connect(sender="router.invalid_query", receiver="query_processor.db_query")

query_pipeline.connect(sender="router.invalid_query", receiver="query_processor.db_output")

payload = {
    "natural_language": "Sales data from October 2023 to December 2023",
    "valid": False,
    "db_query": None,
}


def run_pipeline(payload):
    result = query_pipeline.run(data=payload)
    query_pipeline.draw(path="pipeline_try.png")
    print(result)


run_pipeline(payload)
