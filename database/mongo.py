from pymongo import MongoClient


class MongoDB:
    def __init__(self):
        """
        Description: Initialize the MongoDB database connection
        Args:
            None
        """
        self.client = None
        self.db = None

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
        Description: Connect to the MongoDB database server
        Args:
            None
        """
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["mydatabase"]

    def close(self):
        """
        Description: Close the MongoDB database connection
        Args:
            None
        """
        if self.client is not None:
            self.client.close()

    def execute_query(self, query):
        """
        Description: Execute a query
        Args:
            query (str): The SQL query to execute
        """
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        cur.close()

    def close(self):
        """
        Description: Close the PostgreSQL database connection
        Args:
            None
        """
        if self.conn is not None:
            self.conn.close()

    def insert(self, table, columns, values):
        """
        Description: Insert data into a table
        Args:
            table (str): Name of the table
            columns (list): List of column names
            values (list): List of values
        """
        columns_str = ", ".join(columns)
        values_str = ", ".join(["%s"] * len(values))
        query = f"INSERT INTO {table} ({columns_str}) VALUES ({values_str})"
        cur = self.conn.cursor()
        cur.execute(query, values)
        self.conn.commit()
        cur.close()

    def insert(self, collection, document):
        """
        Description: Insert a document into a collection
        Args:
            collection (str): Name of the collection
            document (dict): Document to insert
        """
        self.db[collection].insert_one(document)

    def find(self, collection, query):
        """
        Description: Find documents in a collection
        Args:
            collection (str): Name of the collection
            query (dict): Query to use for finding documents
        """
        return self.db[collection].find(query)

    def update(self, collection, query, new_values):
        """
        Description: Update documents in a collection
        Args:
            collection (str): Name of the collection
            query (dict): Query to use for finding documents to update
            new_values (dict): New values to set
        """
        self.db[collection].update_many(query, {"$set": new_values})

    def delete(self, collection, query):
        """
        Description: Delete documents from a collection
        Args:
            collection (str): Name of the collection
            query (dict): Query to use for finding documents to delete
        """
        self.db[collection].delete_many(query)

    def get_all_collections(self):
        """
        Description: Get the names of all collections
        """
        return self.db.list_collection_names()

    def get_all_collections_info(self):
        """
        Description: Get the names of all collections and a sample document from each
        """
        collections_info = {}
        for collection in self.db.list_collection_names():
            collections_info[collection] = self.db[collection].find_one()
        return collections_info

    def get_collection_schema(self, collection):
        """
        Description: Get a sample document from a collection to infer its schema
        Args:
            collection (str): Name of the collection
        """
        return self.db[collection].find_one()
