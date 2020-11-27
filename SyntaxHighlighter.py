import json
from os.path import isfile
from re import MULTILINE, compile
from tkinter import Text
from typing import Match


class SyntaxHighlighter:

    def __init__(self, text: Text):
        self.text = text
        self.lexer = ".+"
        self.conditions = []
        self.tags = []

    def load_from_file(self, file: str):
        if not isfile(file):
            return
        with open(file) as syntax_file:
            data = json.loads(syntax_file.read())
            for tag, values in data["tags"].items():
                self.add_condition(tag, values["regex"], values["colour"])

    def add_condition(self, tag_name: str, regex: str, colour: str):
        self.conditions.append(f"(?P<{tag_name}>{regex})")
        self.text.tag_config(tag_name, foreground=colour)
        self.tags.append(tag_name)
        self.lexer = "|".join(self.conditions)

    def add_keywords(self, tag_name: str, words: list[str], colour: str):
        regex = "|".join(words)
        self.add_condition(tag_name, regex, colour)

    def get_match(self, match: Match):
        for group in self.tags:
            if match.groupdict()[group]:
                return group
        return None

    def highlight(self, _all: bool = False):
        if _all:
            start_index = "1.0"
            end_index = "end"
        else:
            start_index = f"{self.text.index('@0,0').split('.')[0]}.0"
            end_index = f"{self.text.index(f'@0,{self.text.winfo_height()}+1line').split('.')[0]}.0"

        for tag in self.tags:
            self.text.tag_remove(tag, start_index, end_index)

        regex = compile(self.lexer, MULTILINE)
        text = self.text.get(start_index, end_index)
        index = 0

        while match := regex.search(text, index):
            group = self.get_match(match)
            self.text.tag_add(group, f"{start_index}+{match.start()}c", f"{start_index}+{match.end()}c")
            index = match.end()
