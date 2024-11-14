class Stats:
    def __init__(self, char_count=0, word_count=0, paragraph_count=0, character_count=0):
        self.char_count = char_count
        self.word_count = word_count
        self.paragraph_count = paragraph_count
        self.characters = character_count
    def __getitem__(self, key):
        if key == "char_count": return self.char_count
        if key == "word_count": return self.word_count
        if key == "paragraph_count": return self.paragraph_count
    def keys(self):
        for key in ["char_count","word_count","paragraph_count"]:
            yield key
    def __setitem__(self, key, value):
        if key == "char_count": 
            self.char_count = value
            return
        if key == "word_count": 
            self.word_count = value
            return
        if key == "paragraph_count": 
            self.paragraph_count = value
            return
    def get(self, key, default):
        try: return self.__getitem__(key)
        except: default
    def __repr__(self):
        return str(self)
    def __str__(self) -> str:
        return f"char_count: {self.char_count},word_count: {self.word_count},paragraph_count: {self.paragraph_count}"
        