""" Make imports from table module easier. """
from .database import Database
from .tables import Table
from .tables import TableManager

__all__ = [
    'Database',
    'Table',
    'TableManager'
]
