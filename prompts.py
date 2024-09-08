import dotenv

from database.postgres import PostgresDB


def connect_to_db():
    """
    Description: Connect to the PostgreSQL database
    Args:
        None
    """
    dotenv.load_dotenv()
    db = PostgresDB()
    db.connect()
    return db


def create_query_processor_prompt(user_prompt: str):
    """
    Description: Create a prompt for the user to input a query
    Args:
        user_prompt (str): The prompt for the user to input
    Output:
        prompt (str) : The prompt for the user to input a query
    """
    db = connect_to_db()
    table_details = db.get_all_table_details()
    return f"""
    You will be given database details and a user prompt.
    Use this prompt to writte a query that will satisfy the needs of the prompt.
    Table Details:\n
            {table_details}\n
    User Prompt:
            {user_prompt}\n
    You need to return the query that will satisfy the user prompt.
    The database being used is a PostgreSQL database.
    """


def create_query_checker_prompt(user_prompt: str, db_query: str, db_output: str):
    """
    Description: Create a prompt to check whether the database output is correct
    Args:
        user_prompt (str): The prompt for the user to input
        db_query (str): The query that needs to be executed
        db_output (str): The output that should be returned
    Output:
        prompt (str) : The prompt for the user to input a query
    """
    return f"""
    You will be given a user prompt, a query, and the output.
    User Prompt:
            {user_prompt}\n
    Query:
            {db_query}\n
    Output:
            {db_output}\n
    Check whether the outout is correct for the given query and user prompt.
    You need to return a boolean value of True if the output is correct, False otherwise.
    """
