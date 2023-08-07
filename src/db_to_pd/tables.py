""" Wrapper for a Database table. """
from typing import List
import csv
import os
import pandas as pd
from .config import load_config
from .database import Database


class Table:
    """
    Represents a table in the database.
    """

    def __init__(self, table_name: str):
        """
        Initializes a new Table object with the given table name.

        Args:
            table_name: The name of the table in the database.
        """
        self.table_name = table_name.lower()

    def to_df(self) -> pd.DataFrame:
        """
        Retrieves the data in the table and returns it as a Pandas dataframe.

        Returns:
            A Pandas dataframe containing the contents of the table.
        """
        database = Database()
        query = f"SELECT * FROM {self.table_name}"
        return database.execute_query(query)

    def save_as_csv(self, path: str = "") -> None:
        """
        Retrieves the data in the table and saves it as a CSV file.

        Args:
            path: The path to the CSV file to save.
        """
        data_frame = self.to_df()
        file_path = self.__get_file_path(extension="csv", path=path)
        print(f"Saving Pandas DataFrame to CSV file: {file_path}")
        data_frame.to_csv(file_path, quoting=csv.QUOTE_ALL, index=False)

    def save_as_excel(self, path: str = "") -> None:
        """
        Retrieves the data in the table and saves it as an Excel file.

        Args:
            path: The path to the Excel file to save.
        """
        data_frame = self.to_df()
        file_path = self.__get_file_path(extension="xlsx", path=path)
        sheet_name = self.__get_valid_sheet_name()
        print(f"Saving Pandas DataFrame to Excel file: {file_path}")
        data_frame.to_excel(file_path, sheet_name=sheet_name, index=False, engine='openpyxl')

    def __get_valid_sheet_name(self, max_length=31):
        """
        In Excel a sheet name can have a max length of 31.

        Trim the sheet name to fit within max_length and add ellipsis if truncated.
        """
        sheet_name = self.table_name
        if len(sheet_name) <= max_length:
            return sheet_name

        # Subtracting 3 for the ellipsis
        return sheet_name[:max_length - 3] + "..."

    def __get_file_path(self, extension: str, path: str = "") -> str:
        """
        Return the file path. By default, use the table name and the given extension.
        """
        if path.endswith(extension):
            return path

        return os.path.join(path, f"{self.table_name}.{extension}")


class TableManager:
    """
    Provides an interface for managing tables in the database.
    """
    def __init__(self, include_views: bool = False):
        """
        Initializes a new TableManager object.
        """
        config = load_config()
        self.schema_name = config['database']['schema']
        self.include_views = include_views
        self._tables = []
        self._populate_tables()

    def _populate_tables(self) -> None:
        """
        Populates the list of tables from the database.
        """
        database = Database()
        table_query = f"""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = '{self.schema_name}'
        """
        view_query = f"""
        SELECT table_name
        FROM information_schema.views
        WHERE table_schema = '{self.schema_name}'
        """

        if self.include_views:
            query = table_query
        else:
            query = table_query + "EXCEPT" + view_query

        result = database.execute_query(query)
        self._tables = [Table(row) for row in result['table_name']]

    def get_table_names(self) -> List[str]:
        """
        Retrieves a list of the names of all tables in the database.

        Returns:
            A list of table names.
        """
        return [table.table_name for table in self._tables]

    def get_table(self, table_name: str) -> Table:
        """
        Retrieves the Table object for the specified table name.

        Args:
            table_name: The name of the table.

        Returns:
            The Table object for the specified table name.
        """
        for table in self._tables:
            if table.table_name == table_name.lower():
                return table
        raise ValueError(f"Table {table_name} not found in database.")

    def get_table_df(self, table_name: str) -> pd.DataFrame:
        """
        Retrieves the data in the table and returns it as a Pandas dataframe.

        Args:
            table_name: The name of the table to get from the database

        Returns:
            A Pandas dataframe containing the contents of the table.
        """
        return self.get_table(table_name).to_df()
