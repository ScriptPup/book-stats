from bs4 import BeautifulSoup, NavigableString
from stats import Stats
from chapter import Chapter
from reports import Reports
from markdown import markdown
import os

root = os.path.dirname(__file__)

class Book:
    def __init__(self
                 , path: str
                 , start_at_chapter: int=0
                 , badwords_list_path: str = f"{root}/badwords"
                 , excludeword_list_path: str = f"{root}/exclude_from_wordlist"
                 , debug=False
                ):
        self.path: str = path
        self.start_at_chapter: int = start_at_chapter
        self.chapters: list[Chapter] = []        
        self.stats: Stats = None
        self._raw_content = None
        self._content = None
        self.badwords_list_path = badwords_list_path
        self.excludeword_list_path = excludeword_list_path
        self.debug = debug
        self.parse()
        self.reports: Reports = Reports(self.chapters)        
    
    @property
    def eligible_bad_words(self):
        with open(self.badwords_list_path, "r") as f: return f.read().split("\n")

    @property
    def words_excluded_from_wordlist(self):
        with open(self.excludeword_list_path, "r") as f: return f.read().split("\n")

    @property
    def raw_content(self) -> str:
        if self._raw_content != None: return self._raw_content
        with open(self.path, "r") as f:
            self._raw_content = str(f.read())
        return self._raw_content
    
    @property
    def content(self) -> BeautifulSoup:
        if self._content != None: return self._content
        self._content = BeautifulSoup(markdown(self.raw_content), features="html.parser")
        return self._content

    def parse(self):
        elements = [element for element in self.content]
        chapter_count = self.start_at_chapter - 1
        chapter_name = ""
        chapter_content = ""
        for element in elements:
            if not isinstance(element, NavigableString):                
                if element.name.lower() == "h1":
                    if chapter_count >= self.start_at_chapter:
                        bs_content = BeautifulSoup(chapter_content, features="html.parser")
                        self.chapters.append(
                            Chapter(chapter_count
                                    , chapter_name
                                    , bs_content
                                    , badwords_list_path = self.badwords_list_path
                                    , excludeword_list_path = self.excludeword_list_path
                                    , debug=self.debug                                    
                            )
                        )
                        if self.debug: print(f"Added chapter {chapter_count}: {chapter_name}")
                    chapter_count += 1
                    chapter_name = element.text
                    if self.debug: print(f"Set chapter scan to Chapter {chapter_count} - {chapter_name}")
                    chapter_content = ""           
                    continue
            chapter_content += str(element)
        bs_content = BeautifulSoup(chapter_content, features="html.parser")
        self.chapters.append(Chapter(chapter_count, chapter_name, bs_content))
        if self.debug: print(f"Added chapter {chapter_count}: {chapter_name}")
        