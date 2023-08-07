""" Handles the database connection. """
from sshtunnel import SSHTunnelForwarder

import psycopg2
import pandas as pd

from .config import load_config


class Database:
    """
    A class for connecting to a Postgres database via an SSH tunnel and executing SQL queries.
    """
    def __init__(self):
        config = load_config()
        ssh_config = config['ssh']
        db_config = config['database']

        # Connect to the SSH tunnel
        self.server = SSHTunnelForwarder(
            ssh_config_file=None,
            ssh_address_or_host=(ssh_config['host'], ssh_config['port']),
            ssh_username=ssh_config['username'],
            ssh_password=ssh_config['password'],
            remote_bind_address=(db_config['host'], db_config['port']),
            allow_agent=False,
            local_bind_address=('127.0.0.1',),
            host_pkey_directories="."  # Set to ignore ssh keys in default directory
        )
        self.server.start()

        # Connect to the Postgres database
        self.conn = psycopg2.connect(
            host=self.server.local_bind_host,
            port=self.server.local_bind_port,
            dbname=db_config['name'],
            user=db_config['user'],
            password=db_config['password']
        )

    def __del__(self):
        """
        Cleans up resources used by the database connection.
        """
        self.conn.close()
        if self.server is not None and self.server.is_active:
            self.server.stop()

    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Executes the given SQL query and returns the results as a Pandas dataframe.

        Args:
            query: The SQL query to execute.

        Returns:
            A Pandas dataframe containing the results of the query.
        """
        return pd.read_sql_query(query, self.conn)
