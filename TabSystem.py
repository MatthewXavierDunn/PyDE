from tkinter import Button, Frame

from settings import styling


class TabSystem(Frame):

    def __init__(self, master):
        super(TabSystem, self).__init__(
            master,
            bg=styling["tab-bg"],
        )

        self.buttons: list[Button] = []
        self.tabs: list[Frame] = []
        self._index = 0
        self._pindex = self._index
        self.button_frame = Frame(
            self,
            bg=styling["tab-gutter"]
        )
        self.button_frame.pack(fill="x", side="top")

        self.master.bind("<Control-Tab>", lambda e: self.next())
        self.master.bind("<Control-Shift-Tab>", lambda e: self.prev())

    @property
    def tab(self):
        return self.tabs[self.index]

    @property
    def button(self):
        return self.buttons[self.index]

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        index = index + len(self.tabs) if index < 0 else index % len(self.tabs)
        self._pindex = self._index
        self._index = index
        self.update_view()

    def add(self, name: str, tab: Frame):
        self.tabs.append(tab)
        button = Button(
            self.button_frame,
            text=name,
            relief="flat",
            fg=styling["fg"],
            font=styling["tab-font"],
            padx=12,
            pady=6,
        )

        button.pack(side="left")
        button.bind("<Button-1>", lambda e: self.select_tab(tab))
        button.bind("<Enter>", lambda e: button.config(bg=styling["tab-hover-bg"]))
        button.bind("<Leave>", lambda e: button.config(
            bg=styling["tab-active-bg"] if self.tab == tab else styling["tab-bg"]
        ))
        self.buttons.append(button)

    def delete(self, index):
        self.tab.destroy()
        self.button.destroy()
        del self.tabs[index]
        del self.buttons[index]
        if self._pindex == self._index:
            if self.tabs:
                self.index = 0
            return
        self.index = self._pindex - 1 if self._pindex > self._index else self._pindex

    def select_tab(self, tab: Frame):
        self.index = self.tabs.index(tab)
        return "break"

    def select(self, index: int):
        self.index = index

    def update_view(self):
        if self._pindex < len(self.tabs):
            self.buttons[self._pindex].config(bg=styling["tab-bg"])
            self.tabs[self._pindex].pack_forget()
        self.button.config(bg=styling["tab-active-bg"])
        self.tab.pack(expand=True, fill="both")

    def next(self):
        self.index += 1
        return "break"

    def prev(self):
        self.index -= 1
        return "break"
