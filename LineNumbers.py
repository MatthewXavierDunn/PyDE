from tkinter import Canvas

from BaseText import BaseText
from settings import styling


class LineNumbers(Canvas):

    def __init__(self, master, text: BaseText):
        super(LineNumbers, self).__init__(
            master,
            width=styling["font"][1] * 5,
            bg=styling["bg"],
            highlightthickness=0,
        )
        self.text = text

    def redraw(self):
        self.delete("all")
        i = self.text.index("@0,0")
        current_line = self.text.index("insert").split(".")[0]
        x = styling["font"][1] * len(str(self.text.line_num))
        while dline := self.text.dlineinfo(i):
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(
                x, y,
                anchor="ne",
                text=linenum,
                fill=styling["active-linenum-fg"] if current_line == linenum else styling["linenum-fg"],
                font=styling["font"],
            )
            i = self.text.index(f"{i}+1line")
