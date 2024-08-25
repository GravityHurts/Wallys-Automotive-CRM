import tkinter as tk

class TextWithVar(tk.Text):
    def __init__(self, master=None, cnf={}, **kw):
        self.textvariable = kw.pop('textvariable', None)
        super().__init__(master, cnf, **kw)
        self.config(height=10)
        if self.textvariable is not None:
            self.bind('<<Modified>>', self.on_text_change)
            self.bind('<KeyRelease>', self.on_text_change)
            self.update_textvariable()

    def on_text_change(self, event=None):
        if self.textvariable is not None:
            text = self.get("1.0", "end-1c")
            self.textvariable.set(text)

    def update_textvariable(self):
        if self.textvariable is not None:
            self.delete("1.0", "end")
            self.insert("1.0", self.textvariable.get())
