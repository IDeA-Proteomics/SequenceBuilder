import tkinter as tk
from tkinter import ttk
import SequenceSettings as settings


class LabelAndText(tk.Frame):

    def __init__(self, parent, label, textvariable):
        self.parent = parent

        tk.Frame.__init__(self, self.parent)

        self.label = tk.Label(self, text=label)
        self.text = tk.Label(self, textvariable=textvariable)

        self.label.pack(side=tk.LEFT)
        self.text.pack(side=tk.LEFT)

        return
    
class PreAndPostCheck(tk.Frame):

    def __init__(self, parent, label, preVariable, postVariable):
        self.parent = parent

        tk.Frame.__init__(self, self.parent)

        self.label = tk.Label(self, text=label)
        self.pre = tk.Checkbutton(self, text="pre", variable=preVariable, onvalue=1, offvalue=0)
        self.post = tk.Checkbutton(self, text="post", variable=postVariable, onvalue=1, offvalue=0)

        self.label.pack(side=tk.LEFT)
        self.pre.pack(side=tk.LEFT)
        self.post.pack(side=tk.LEFT)

        return
