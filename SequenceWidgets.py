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

    def __init__(self, parent, label, preVariable, postVariable, onChange):
        self.parent = parent

        tk.Frame.__init__(self, self.parent)
        self.onChange = onChange

        self.label = tk.Label(self, text=label)
        self.pre = tk.Checkbutton(self, text="pre", variable=preVariable, onvalue=1, offvalue=0, command=self.onChange)
        self.post = tk.Checkbutton(self, text="post", variable=postVariable, onvalue=1, offvalue=0, command=self.onChange)

        self.label.pack(side=tk.LEFT)
        self.pre.pack(side=tk.LEFT)
        self.post.pack(side=tk.LEFT)

        return

class TrayPicker(tk.Frame):

    def __init__(self, parent, textvariable, onChange, initial_val):
        self.parent = parent

        tk.Frame.__init__(self, self.parent)
        self.textvariable = textvariable
        self.onChange = onChange

        self.buttons = [
            tk.Radiobutton(self, text="", var=self.textvariable, value="R", fg='black', bg='red', width = 4, command=self.onChange),
            tk.Radiobutton(self, text="", var=self.textvariable, value="G", fg='black', bg='green', width = 4, command=self.onChange),
            tk.Radiobutton(self, text="", var=self.textvariable, value="B", fg = 'black', bg='blue', width = 4, command=self.onChange),
            tk.Radiobutton(self, text="", var=self.textvariable, value="Y", fg = 'black', bg='yellow', width = 4, command=self.onChange)
        ]
        for button in self.buttons:
            button.pack(side = tk.LEFT)
            if button.cget('value') == initial_val:
                button.select()

        return
    
    def refreshState(self, trays):
        for button in self.buttons:
            if button.cget('value') in trays:
                button.config(state="normal")
            else:
                button.config(state="disabled")
                if button.cget('value') == self.textvariable.get():
                    self.textvariable.set(trays[1])
                    self.onChange()
        return