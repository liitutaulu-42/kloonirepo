from typing import NamedTuple, Optional

class Article(NamedTuple):
    key: str
    author: str
    title: str
    journal: str
    year: str
    month: Optional[str] = None
    volume: Optional[str] = None
    number: Optional[str] = None
    pages: Optional[str] = None
    note: Optional[str] = None

class Book(NamedTuple):
    key: str
    author: str
    title: str
    year: str
    publisher: str
    address: str
