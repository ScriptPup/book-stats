from bs4 import BeautifulSoup, NavigableString
from .stats import Stats
import re, os, sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        # Running as bundled executable
        base_path = os.path.dirname(sys.executable)
    else:
        # Running in development
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)

class Chapter:
    def __init__(self
                 , number: int
                 , name: str
                 , content: BeautifulSoup
                 , badwords_list_path: str = f"{resource_path('badwords')}"
                 , excludeword_list_path: str = f"{resource_path('exclude_from_wordlist')}"
                 , debug: bool=False
        ):
        self.number: int = number
        self.name: str = name
        self.content: BeautifulSoup = content
        self._stats: Stats|None = None
        self.all_words: dict = {}
        self.debug = debug
        self.badwords_list_path = badwords_list_path
        self.excludeword_list_path = excludeword_list_path

    
    @property
    def words(self) -> dict:
        exclude_words = self.words_excluded_from_wordlist
        return {k: v for k,v in self.all_words.items() if k.lower() not in exclude_words}
    
    @property
    def bad_words(self) -> dict:
        badwords = self.eligible_bad_words
        return {k: v for k,v in self.all_words.items() if k.lower() in badwords}

    @property
    def stats (self) -> Stats:
        if self._stats == None: self.__gather_stats()
        return self._stats
    
    @property
    def eligible_bad_words(self):
        with open(os.path.abspath(self.badwords_list_path), "r") as f: return f.read().split("\n")

    @property
    def words_excluded_from_wordlist(self):
        with open(os.path.abspath(self.excludeword_list_path), "r") as f: return f.read().split("\n")
        
    def __gather_stats(self):
        self._stats = Stats()
        self.all_words: dict = {}        
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
        self.stats.badword_count = sum([bw for bw in self.bad_words.values()])

    def AddWord(self, word) -> bool:
        wrd = re.sub("[^a-zA-Z0-9\s\:]","",word).lower()
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