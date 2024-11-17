from bs4 import BeautifulSoup, NavigableString
from .stats import Stats
from .chapter import Chapter
from .reports import Reports
from markdown import markdown

class Book:
    def __init__(self, path: str, start_at_chapter: int=0, debug=False):
        self.path: str = path
        self.start_at_chapter: int = start_at_chapter
        self.chapters: list[Chapter] = []        
        self.stats: Stats = None
        self._raw_content = None
        self._content = None
        self.debug = debug
        self.parse()
        self.reports: Reports = Reports(self.chapters)
    
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
                        self.chapters.append(Chapter(chapter_count, chapter_name, bs_content, debug=self.debug))
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
        