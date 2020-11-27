from os import getcwd
from tkinter import Frame
from tkinter.filedialog import askopenfile
from tkinter.messagebox import askyesno
from typing import Optional, TextIO

from CodeEditor import CodeEditor
from TabSystem import TabSystem


class Application(Frame):

    def __init__(self, master):
        super(Application, self).__init__(master, background="#000")
        self.tabs = TabSystem(self)
        self.tabs.pack(expand=True, fill="both")

        self.master.bind("<Control-s>", lambda e: self.save_file())
        self.master.bind("<Control-n>", lambda e: self.new_tab())
        self.master.bind("<Control-o>", lambda e: self.open_file())
        self.master.bind("<Control-w>", lambda e: self.close_tab())
        self.master.bind("<Control-Tab>", lambda e: self.next_tab())
        self.master.bind("<Control-Shift-Tab>", lambda e: self.prev_tab())

        self.new_tab()

    def new_tab(self, file: Optional[TextIO] = None):
        tab = CodeEditor(self.tabs, self, file)
        self.tabs.add(tab.name, tab)
        self.tabs.select_tab(tab)

    def save_file(self):
        self.tabs.tab.save()
        self.tabs.button["text"] = self.tabs.tab.name

    def open_file(self, path=None):
        file = open(path) if path else askopenfile(
            mode="r+",
            initialdir=getcwd(),
            filetypes=(
                ("Python File", "*.py"),
                ("All Files", "*.*")
            )
        )
        if not file:
            return
        if self.tabs.tab.saved and self.tabs.tab.file is None:
            self.close_tab(len(self.tabs.tabs) == 1)
        self.new_tab(file)

    def close_tab(self, force_close: bool = False):
        if not self.tabs.tab.saved:
            save_file = askyesno(
                title="Unsaved File",
                message=f'Document "{self.tabs.tab.name}" not saved! Save changes?'
            )
            if save_file:
                self.tabs.tab.save()
                if not self.tabs.tab.saved:
                    return
        self.tabs.delete(self.tabs.index)
        if force_close:
            return
        if not self.tabs.tabs:
            self.new_tab()

    def next_tab(self):
        self.tabs.next()
        self.tabs.tab.text.focus()
        return "break"

    def prev_tab(self):
        self.tabs.prev()
        self.tabs.tab.text.focus()
        return "break"
