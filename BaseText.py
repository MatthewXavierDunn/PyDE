from tkinter import Text

from _tkinter import TclError

from settings import styling


class BaseText(Text):

    def __init__(self, master):
        super(BaseText, self).__init__(
            master,
            exportselection=True,
            undo=True,
            maxundo=-1,
            relief="flat",
            bg=styling["bg"],
            fg=styling["fg"],
            insertbackground=styling["insert-bg"],
            insertwidth=styling["insert-w"],
            selectbackground=styling["select-bg"],
            font=styling["font"],
            wrap=styling["wrap"],
        )
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    @property
    def line_num(self) -> int:
        return len(self.get("1.0", "end").split("\n")) - 1

    def _proxy(self, *args):
        cmd = (self._orig,) + args
        if args == ("delete", "sel.first", "sel.last") and self.tag_ranges("sel") == ():
            return 0

        try:
            result = self.tk.call(cmd)
        except TclError:
            return 0

        text_changed = args[0] in ("insert", "replace", "delete")

        if text_changed:
            self.event_generate("<<TextModified>>", when="tail")
            self.edit_separator()

        if text_changed or \
                args[0:3] == ("mark", "set", "insert") or \
                args[0:2] == ("xview", "moveto") or \
                args[0:2] == ("xview", "scroll") or \
                args[0:2] == ("yview", "moveto") or \
                args[0:2] == ("yview", "scroll"):
            self.event_generate("<<Change>>", when="tail")

        return result
