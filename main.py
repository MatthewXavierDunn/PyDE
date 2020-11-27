from tkinter import Tk

from Application import Application

if __name__ == "__main__":
    root = Tk()
    root.title("PyDE")
    app = Application(root)
    app.pack(expand=True, fill="both")
    root.mainloop()
