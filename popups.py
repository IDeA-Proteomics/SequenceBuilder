import tkinter as tk
import openpyxl


class AskHeaderRow(tk.Toplevel):

    def __init__(self, parent, sh):

        self.parent = parent
        tk.Toplevel.__init__(self, self.parent)

        self.sh = sh

        self.choice = tk.StringVar(value="None")

        self.top_frame = tk.Frame(self)
        self.label = tk.Label(self.top_frame, text="Could not find header row.\n  Please select the header for sample number.")
        self.label.pack()
        self.top_frame.pack()

        self.row_frame = tk.Frame(self)
        self.row_frame.pack()

        self.button_frame = tk.Frame(self)
        self.button_frame.pack()

        self.row = 0

        self.displayRow()

        self.done_button = tk.Button(self.button_frame, text="Done", command=self.onDone)
        self.done_button.pack(side=tk.LEFT)
        self.next_button = tk.Button(self.button_frame, text="Next Row", command=self.displayRow)
        self.next_button.pack(side=tk.LEFT)

        self.transient(self.parent)
        self.grab_set()
        self.parent.wait_window(self)

        return

    def onDone(self):
        self.destroy()

    def displayRow(self):
        for w in self.row_frame.winfo_children():
            w.destroy()
        self.row += 1

        for i in range(1, self.sh.max_column + 1):
            name = self.sh.cell(row = self.row, column = i).value
            rad = tk.Radiobutton(self.row_frame, text=name, var=self.choice, value=name)
            rad.pack()


class askNameColumn(tk.Toplevel):

    def __init__(self, parent, sh, row):

        self.parent = parent
        tk.Toplevel.__init__(self, self.parent)

        self.sh = sh

        self.choice = tk.StringVar(value="None")

        self.top_frame = tk.Frame(self)
        self.label = tk.Label(self.top_frame, text="Please select header for Sample Name")
        self.label.pack()
        self.top_frame.pack()

        self.row_frame = tk.Frame(self)
        self.row_frame.pack()

        self.button_frame = tk.Frame(self)
        self.button_frame.pack()

        self.row = row

        self.displayRow()

        self.done_button = tk.Button(self.button_frame, text="Done", command=self.onDone)
        self.done_button.pack(side=tk.LEFT)

        self.transient(self.parent)
        self.grab_set()
        self.parent.wait_window(self)

        return

    def onDone(self):
        self.destroy()

    def displayRow(self):

        for i in range(1, self.sh.max_column + 1):
            name = self.sh.cell(row = self.row, column = i).value
            rad = tk.Radiobutton(self.row_frame, text=name, var=self.choice, value=name)
            rad.pack()




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