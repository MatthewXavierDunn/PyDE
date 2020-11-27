from os import getcwd, system
from re import search
from tkinter import Frame, Scrollbar
from tkinter.filedialog import asksaveasfile
from typing import Optional, TextIO

from BaseText import BaseText
from LineNumbers import LineNumbers
from SyntaxHighlighter import SyntaxHighlighter
from settings import styling


class CodeEditor(Frame):

    def __init__(self, master, parent, file: Optional[TextIO] = None):
        super(CodeEditor, self).__init__(
            master,
            bg=styling["bg"],
        )

        self.parent = parent
        self.file = file

        self.text = BaseText(self)
        self.line_nums = LineNumbers(self, self.text)
        self.scrollbar = Scrollbar(self, command=self.text.yview)

        self.line_nums.pack(side="left", fill="y", padx=12)
        self.scrollbar.pack(side="right", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.config(yscrollcommand=self.scrollbar.set)

        if self.file:
            self.text.insert("1.0", self.file.read())
        self._saved_data = self.data
        self._p_text = self.data

        self.highlighter = SyntaxHighlighter(self.text)
        self.highlighter.load_from_file(f"packages/highlighting/{self.type}.json")

        # override default shortcuts
        self.override("<Control-o>", self.parent.open_file)
        self.override("<Control-h>")
        self.override("<Control-/>")
        self.override("<Control-t>")
        self.override("<Control-i>")
        self.override("<Control-d>")
        self.override("<Control-k>")

        # custom shortucts
        self.listen("<Control-z>", self.text.edit_undo)
        self.listen("<Control-Shift-z>", self.text.edit_redo)
        self.listen("<F5>", self.run_file)

        # bracket/quotation completion
        self.listen("(", self.complete_bracket, ("(", ")"))
        self.listen("[", self.complete_bracket, ("[", "]"))
        self.listen("{", self.complete_bracket, ("{", "}"))
        self.listen("'", self.complete_bracket, ("'", "'"))
        self.listen('"', self.complete_bracket, ('"', '"'))
        self.listen(")", self.close_bracket, ")")
        self.listen("]", self.close_bracket, "]")
        self.listen("}", self.close_bracket, "}")

        # custom whitespace editing
        self.listen("<Return>", self.handle_return)
        self.listen("<BackSpace>", self.handle_backspace)
        self.listen("<Tab>", self.handle_tab)

        self.listen("<<Change>>", self.on_change)
        self.listen("<Configure>", self.on_change)

        self.text.focus()
        self.highlighter.highlight(True)

    @property
    def data(self) -> str:
        return self.text.get("1.0", "end")

    @property
    def name(self) -> str:
        return search(r"^[A-Z]:/(?:\w+/)*(\w*.\w+)$", self.file.name).group(1) if self.file else "New File"

    @property
    def type(self) -> Optional[str]:
        return self.file.name.split(".")[-1] if self.file else None

    @property
    def saved(self) -> bool:
        return self._saved_data == self.data

    def __del__(self):
        if self.file:
            self.file.close()

    def listen(self, event: str, func, args=None):
        if args:
            self.text.bind(event, lambda e: func(*args))
            return
        self.text.bind(event, lambda e: func())

    def override(self, event: str, func=None):

        def ptp(f=lambda: ()):
            f()
            return "break"

        if func:
            self.text.bind(event, lambda e: ptp(func))
        return "break"

    def run_file(self):
        self.save()
        if self.file is None:
            return
        if self.type == "py":
            system(f"python {self.file.name}")

    def save(self):
        if self.file:
            self.file.seek(0)
            self.file.write(self.data[:-1])
            self.file.truncate()
        else:
            self.file = asksaveasfile(mode="w+", initialdir=getcwd(), defaultextension=".py")
        self._saved_data = self.data if self.file else self._saved_data

    def on_change(self):
        self.line_nums.redraw()
        if self._p_text == self.data:
            return
        self._p_text = self.data
        self.highlighter.highlight()

    def delete_selection(self) -> bool:
        if self.text.tag_ranges("sel"):
            self.text.delete("sel.first", "sel.last")
            return True
        return False

    def get_indentation(self, index: str) -> int:
        insert_line_index = self.text.index(index).split(".")[0]
        return self.text.get(f"{insert_line_index}.0", f"{insert_line_index}.end").count("    ")

    def handle_tab(self):
        self.delete_selection()
        self.text.insert("insert", "    ")
        return "break"

    def handle_backspace(self):
        if self.delete_selection():
            return "break"
        if self.text.get("insert-4c", "insert") == "    ":
            self.text.delete("insert-4c", "insert")
        elif self.text.get("insert-1c", "insert+1c") in ["()", "[]", "{}"]:
            self.text.delete("insert-1c", "insert+1c")
        else:
            self.text.delete("insert-1c")
        return "break"

    def handle_return(self):
        self.delete_selection()
        indentation = self.get_indentation("insert")
        if self.text.get("insert-1c", "insert") == ":":
            self.text.insert("insert", f"\n{'    ' * (indentation + 1)}")
        elif self.text.get("insert-1c", "insert+1c") in ["()", "[]", "{}"]:
            self.text.insert("insert", f"\n{'    ' * (indentation + 1)}\n{'    ' * indentation}")
            index = self.text.index("insert-1line").split(".")[0]
            self.text.mark_set("insert", f"{index}.end")
        else:
            self.text.insert("insert", f"\n{'    ' * indentation}")
        return "break"

    def complete_bracket(self, open_bracket: str, close_bracket: str):
        if open_bracket == close_bracket and self.text.get("insert") == close_bracket:
            self.close_bracket(close_bracket)
            return "break"
        if self.text.tag_ranges("sel"):
            self.text.insert("sel.first", open_bracket)
            self.text.insert("sel.last", close_bracket)
        else:
            self.text.insert("insert", open_bracket + close_bracket)
            self.text.mark_set("insert", "insert-1c")
        return "break"

    def close_bracket(self, close_bracket: str):
        if self.text.get("insert") == close_bracket:
            self.text.mark_set("insert", "insert+1c")
            return "break"
