from bs4 import BeautifulSoup, NavigableString
from .stats import Stats
import re

class Chapter:
    def __init__(self, number: int, name: str, content: BeautifulSoup, debug: bool=False):
        self.number: int = number
        self.name: str = name
        self.content: BeautifulSoup = content
        self._stats: Stats|None = None
        self.all_words: dict = {}
        self.debug = debug
    
    @property
    def stats (self) -> Stats:
        if self._stats == None: self.__gather_stats()
        return self._stats
        
    def __gather_stats(self):
        self._stats = Stats()
        for element in self.content:
            word_count = 0
            for word in element.text.split(' '):
                if not (word == '' or word == None or word == '\n'):
                    if self.AddWord(word):
                        word_count += 1
            self.stats.char_count += len(element.text)            
            self.stats.word_count += word_count
            if not isinstance(element, NavigableString):
                paragraph_count = 1 if len(element.text) > 0 and not element.find("em") and element.text != '\n' and element != '\n' else 0                
                self.stats.paragraph_count += paragraph_count
        words = self.all_words
        self.all_words = dict(sorted(words.items(), key=lambda item: item[1], reverse=True))

    def AddWord(self, word) -> bool:
        wrd = re.sub("[^a-zA-Z0-9\s\:]","",word)
        if wrd == "" or wrd == None: 
            if self.debug: print(f"Ignoring {word}")
            return False
        if wrd not in self.all_words: 
            self.all_words[wrd] = 0
        self.all_words[wrd] += 1
        return True

    def __str__(self) -> str:
        return f"Chapter {self.number} - {self.name}"
    
    def __repr__(self) -> str:
        return str(self)