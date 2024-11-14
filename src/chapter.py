from bs4 import BeautifulSoup
from .stats import Stats

class Chapter:
    def __init__(self, number: int, name: str, content: BeautifulSoup):
        self.number: int = number
        self.name: str = name
        self.content: BeautifulSoup = content
    
    def __str__(self) -> str:
        return f"Chapter {self.number} - {self.name}"
    
    def __repr__(self) -> str:
        return str(self)