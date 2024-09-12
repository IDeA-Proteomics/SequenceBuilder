import tkinter as tk

class AskProjName(tk.Toplevel):

    def __init__(self, parent):
        self.parent = parent
        tk.Toplevel.__init__(self, self.parent)

        self.frame = tk.Frame(self)

        self.label = tk.Label(self.frame, text="Please Enter a Project Name")
        self.label.pack()

        self.entry = tk.Entry(self.frame, width=50)
        self.entry.pack()

        self.button = tk.Button(self.frame, text="OK", command=self.onOk)
        self.button.pack()


        self.frame.pack()

        self.transient(self.parent)
        self.grab_set()
        self.parent.wait_window(self)

        return

    def onOk(self):
        self.result = self.entry.get()
        self.destroy()