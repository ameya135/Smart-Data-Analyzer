import json
import logging
import os

import psycopg2

logging.basicConfig(level=logging.INFO)


class PostgresDB:
    def __init__(self):
        """
        Description: Initialize the PostgreSQL database connection
        Args:
            None
        """
        self.conn = None

    # For the context manager class to enable easy testing
    def __enter__(self):
        """
        Description: Enter the context manager
        Args:
            None
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Description: Exit the context manager
        Args:
            None
        """
        self.close()

    def connect(self):
        """
        Description: Connect to the PostgreSQL database server
        Args:
            None
        """
        self.conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )

    def insert(self, table, columns, values):
        """
        Description: Insert data into a table
        Args:
            table (str): Name of the table
            columns (list): List of columns to insert data into
            values (list): List of values to insert into the columns
        """
        try:
            with self.conn.cursor() as cur:
                query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
                cur.execute(query, values)
                self.conn.commit()
        except Exception as e:
            logging.error(e)
            # logging.error(f"Failed to insert data into {table}. Error: {e}")

    def delete(self, table, condition):
        """
        Description: Delete data from a table
        Args:
            table (str): Name of the table
            condition (str): Condition to delete data from the table
        """
        try:
            with self.conn.cursor() as cur:
                query = f"DELETE FROM {table} WHERE {condition}"
                cur.execute(query)
                self.conn.commit()
        except Exception as e:
            logging.error(e)

    def update(self, table, set_values, condition):
        """
        Description: Update data in a table
        Args:
            table (str): Name of the table
            set_values (str): Values to update in the table
            condition (str): Condition to update data in the table
        """
        try:
            with self.conn.cursor() as cur:
                query = f"UPDATE {table} SET {set_values} WHERE {condition}"
                cur.execute(query)
                self.conn.commit()
        except Exception as e:
            logging.error(f"Failed to update data in {table}. Error: {e}")

    def select(self, table, columns, condition=None):
        """
        Description: Select data from a table
        Args:
            table (str): Name of the table
            columns (list): List of columns to select from
            condition (str): Condition to select data from the table
        """
        try:
            with self.conn.cursor() as cur:
                query = f"SELECT {', '.join(columns)} FROM {table}"
                if condition:
                    query += f" WHERE {condition}"
                cur.execute(query)
                return cur.fetchall()
        except Exception as e:
            logging.error(f"Failed to select data from {table}. Error: {e}")

    def select_all(self, table):
        """
        Description: Select all data from a table
        Args:
            table (str): Name of the table
        """
        return self.select(table, ["*"])

    def run_sql(self, query):
        """
        Description: Run a SQL query
        Args:
            query (str): SQL query to run
        """
        cur = self.conn.cursor()
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        list_of_dicts = [dict(zip(columns, row)) for row in rows]
        json_data = json.dumps(list_of_dicts, indent=4, default=self.date_time_handler)

        return str(json_data)

    def date_time_handler(self, obj):
        """
        Description: Convert datetime object to string
        Args:
            obj (datetime): Datetime object
        """
        return obj.isoformat() if hasattr(obj, "isoformat") else obj

    def get_table_details(self, table):
        """
        Description: Get the details of a table
        Args:
            table (str): Name of the table
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table}'"
                )
                return cur.fetchall()
        except Exception as e:
            logging.error(f"Failed to get table details. Error: {e}")

    def get_all_table_names(self):
        """
        Description: Get the names of all tables
        Args:
            None
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
                )
                return cur.fetchall()
        except Exception as e:
            logging.error(f"Failed to get table names. Error: {e}")

    def get_all_table_details(self):
        """
        Description: Get the details of all tables
        Args:
            None
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_schema = 'public'"
                )
                return cur.fetchall()
        except Exception as e:
            logging.error(f"Failed to get table details. Error: {e}")

    def close(self):
        """
        Description: Close the connection to the PostgreSQL database server
        Args:
            None
        """
        if self.conn is not None:
            self.conn.close()
