import tkinter as tk
from IDeA_classes import SampleList


class LabelAndText(tk.Frame):

    def __init__(self, parent, label, text):
        self.parent = parent

        tk.Frame.__init__(self, self.parent)

        self.label = tk.Label(self, text=label)
        self.text = tk.Label(self, text=text)

        self.label.pack(side=tk.LEFT)
        self.text.pack(side=tk.LEFT)

        return

class SFE_Head(tk.Frame):

    def __init__(self, parent, sample_list):

        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        self.path_label = LabelAndText(self, "Path:", sample_list.abs_path)
        self.path_label.pack(side = tk.TOP, anchor=tk.W)

        self.proj_label = LabelAndText(self, "Project:", sample_list.project_name)
        self.proj_label.pack(side=tk.TOP, anchor=tk.W)

        return
    
class SFE_ListText(tk.Text):

    def __init__(self, parent, sample_list):

        self.parent = parent
        self.scrollbar = tk.Scrollbar(self.parent)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Text.__init__(self, self.parent, height=10, width=50, yscrollcommand=self.scrollbar.set)  
        self.scrollbar.config(command=self.yview)
        

        for name in sample_list.samplenames:
            self.insert(tk.END, name + '\n')
        

        return
    

class SFE_ListFrame(tk.Frame):

    def __init__(self, parent, sample_list):

        self.parent = parent    
        tk.Frame.__init__(self, self.parent)

        sfe_list_text = SFE_ListText(self, sample_list)
        sfe_list_text.pack()
        # sfe_list_text.insert(tk.END, "Text Here")

        return
    
    
class SFE_OptionFrame(tk.Frame):

    def __init__(self, parent):

        self.parent = parent
        tk.Frame.__init__(self.parent)

        return
    

class SequenceFrontEnd:

    def __init__(self, parent, sample_list):

        # self.sample_list = sample_list

        self.parent = parent

        self.label = tk.Label(self.parent, text = "Hello World")
        self.label.pack()

        self.head = SFE_Head(self.parent, sample_list)
        self.head.pack(side = tk.TOP, anchor=tk.W)

        self.list_frame = SFE_ListFrame(self.parent, sample_list)
        self.list_frame.pack()

        self.exit_button = tk.Button(self.parent, text = "Exit", command = parent.destroy)
        self.exit_button.pack()


        

def showSeqFE(sample_list):
    root = tk.Tk()
    front_end = SequenceFrontEnd(root, sample_list)
    root.mainloop()

def main():
    showSeqFE()

if (__name__ == "__main__"):
    main()