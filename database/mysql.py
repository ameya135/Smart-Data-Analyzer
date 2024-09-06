import datetime
import json

import pymysql


class MySQLDB:
    def __init__(self, host, dbname, user, password, port=3306):
        """
        Description: Initialize connection to the database
        Args:
            host (str): Host name
            dbname (str): Database name
            user (str): Username
            password (str): Password
            port (int): Port number (default is 3306)
        """
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=dbname,
            port=port,
            cursorclass=pymysql.cursors.DictCursor,
        )

    def select(self, table, columns):
        """
        Description: Select data from a table
        Args:
            table (str): Name of the table
            columns (list): List of columns to select
        """
        try:
            cur = self.conn.cursor()
            query = f"SELECT {', '.join(columns)} FROM {table}"
            cur.execute(query)
            rows = cur.fetchall()
            return rows
        except Exception as e:
            return str(e)

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
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            list_of_dicts = [dict(zip(columns, row)) for row in rows]
            json_data = json.dumps(
                list_of_dicts, indent=4, default=self.date_time_handler
            )
            return str(json_data)
        except Exception as e:
            return str(e)

    def date_time_handler(self, obj):
        """
        Description: Convert datetime object to string
        Args:
            obj (datetime): Datetime object
        """
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))

    def get_table_details(self, table):
        """
        Description: Get the details of a table
        Args:
            table (str): Name of the table
        """
        with self.conn.cursor() as cur:
            cur.execute(f"DESCRIBE {table}")
            return cur.fetchall()

    def get_all_table_details(self):
        """
        Description: Get the details of all tables
        Args:
            None
        """
        with self.conn.cursor() as cur:
            cur.execute("SHOW TABLES")
            tables = cur.fetchall()
            table_details = {}
            for table in tables:
                table_name = table["Tables_in_test"]
                table_details[table_name] = self.get_table_details(table_name)
            return table_details

    def get_all_table_names(self):
        """
        Description: Get the names of all tables
        Args:
            None
        """
        with self.conn.cursor() as cur:
            cur.execute("SHOW TABLES")
            return cur.fetchall()
