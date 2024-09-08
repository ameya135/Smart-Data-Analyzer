from haystack import component


@component
class QueryChecker:
    """
    A component to check if the query is valid. If not valid, send a suggestion back.
    Else, forward the query to the next component.
    """

    @component.output_types(final_report=str, suggestion=str)
    def run(self, report: str):
        if self.is_valid_query(report):
            return {"final_report": report, "suggestion": None}
        else:
            return {
                "final_report": None,
                "suggestion": "Please check your query and try again.",
            }

    def is_valid_query(self, report: str) -> bool:
        # Add logic here to validate the query
        # For now, we assume the query is always valid
        return True
