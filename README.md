db-to-pd
==============================

`db_to_pd` is a Python package that simplifies connecting to a Postgres database, over SSH, and 
retrieving data from it as Pandas dataframes. It includes an easy-to-use interface for managing tables in the
database and provides methods for retrieving and saving data.

Installation
------------

> As this is still experimental there is no PyPI package published yet

To install `db-to-pd` from git, run the following command:

```
python -m pip install "db-to-pd @ git+https://github.com/irsital/db-to-pd.git"
```


Usage
-----

To use `db_to_pd`, you will need to create a `.env` file in the root directory of your
project that contains the necessary configuration information for connecting to your Postgres
database and the SSH tunnel connection details.

If you don't put the `.env` in the root. You can also set the `ENV_FILE_PATH` environment 
variable to the `.env` location.

```text
DATABASE_HOST=your_database_host
DATABASE_PORT=your_database_port
DATABASE_NAME=your_database_name
DATABASE_USER=your_database_username
DATABASE_SCHEMA=your_database_schema
DATABASE_PASSWORD=your_database_password

SSH_HOST=your_ssh_host
SSH_PORT=22
SSH_USERNAME=your_ssh_username
SSH_PASSWORD=your_ssh_password
```

After creating the `.env` file, you can use the `TableManager` class to manage tables in your database. Here's an example of how to use `db_to_pd` to retrieve data from a table in the database:

```python
from db_to_pd import TableManager

# Create a TableManager object
tm = TableManager()  # by default ignores table views

# Get a list of table names in the database
table_names = tm.get_table_names()

# Get a specific Table by name
my_table = tm.get_table('my_table')

# Get the contents of the table as a Pandas dataframe
my_df = my_table.to_df()

# Save the contents of the table as a CSV file
my_table.save_as_csv()  # you can optionally give it a filepath

# But you're probably going to view the contents in Excel, so you can also save it as an Excel file
my_table.save_as_excel() # you can optionally give it a filepath

# If you don't care about the Table functionality, directly get a Pandas DataFrame for a given table name
my_other_table_as_df = tm.get_table_df('my_other_table')
```

You can also use the `Database` class directly to execute SQL queries against the database, and get
the result back as pandas DataFrame:

```python
from db_to_pd import Database

# Create a Database object
db = Database()

# Execute a SQL query against the database, the result is a pandas DataFrame.
result_df = db.execute_query('SELECT * FROM my_table')
```

Development
-----------

If you want to develop this library further you can set up your development environment as follows:

```bash
git clone https://github.com/irsital/db-to-pd.git
cd db-to-pd
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e .
```