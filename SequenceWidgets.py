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