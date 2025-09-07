import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog, Menu

from datamodel import *
from SequenceWidgets import *
from OptionFrame import *
from popups import EditMethodsDialog, SettingsDialog


frame_options = {'highlightbackground':'black' , 'highlightthickness':1}



class HeaderFrame(tk.Frame):

    def __init__(self, parent, datamodel):

        self.parent = parent
        self.datamodel = datamodel
        tk.Frame.__init__(self, self.parent)

        self.path_label = LabelAndText(self, "Path:", textvariable=self.datamodel.sample_list_path_var)
        self.path_label.pack(side = tk.TOP, anchor=tk.W)
        self.project_label = LabelAndText(self, "Project:", textvariable=self.datamodel.project_name_var)
        self.project_label.pack(side=tk.TOP, anchor=tk.W)

        return
    
class InstrumentFrame(tk.Frame):

    def __init__(self, parent, datamodel, onChange = None, onEdit=None):

        self.parent = parent
        self.datamodel = datamodel
        self.onChange = onChange
        tk.Frame.__init__(self, self.parent)

        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side=tk.TOP)
        
        self.instrument_combo = ttk.Combobox(self.top_frame, textvariable=self.datamodel.getOptionVar('instrument'), values=list(self.datamodel.instrument_list), state='readonly', width=20)
        self.instrument_combo.pack(side=tk.LEFT, anchor=tk.NE)
        self.instrument_combo.bind('<<ComboboxSelected>>', self.onInstrumentChange)

        self.dda_button = tk.Radiobutton(self.top_frame, text="DDA", var=datamodel.getOptionVar('diadda'), value="DDA", command=self.onInstrumentChange)
        self.dia_button = tk.Radiobutton(self.top_frame, text="DIA", var=datamodel.getOptionVar('diadda'), value="DIA", command=self.onInstrumentChange)
        self.dda_button.pack(side=tk.LEFT, anchor=tk.E)
        self.dia_button.pack(side=tk.LEFT, anchor=tk.E)

        self.edit_methods_button = tk.Button(self.top_frame, text="Edit Method List", command=onEdit)
        self.edit_methods_button.pack(side=tk.LEFT, anchor=tk.E, padx=30)

        self.method_combo = ttk.Combobox(self, textvariable=self.datamodel.getOptionVar('method'), values=self.datamodel.method_list, state='readonly', width=100)
        self.method_combo.pack(side=tk.TOP, anchor=tk.E)

        self.onInstrumentChange()

        return
    
    def onInstrumentChange(self, event=None):
        self.datamodel.onInstrumentSelection()
        self.method_combo.config(values=self.datamodel.method_list)
        if self.onChange is not None:
            self.onChange()
        return
    
class ListFrame(tk.Frame):

    def __init__(self, parent, datamodel):

        self.parent = parent    
        self.datamodel = datamodel
        tk.Frame.__init__(self, self.parent)

        self.tabs = ttk.Notebook(self)
        self.plate_tab = tk.Frame(self.tabs)
        self.sequence_tab = tk.Frame(self.tabs)

        self.tabs.add(self.plate_tab, text = "Plate")
        # self.tabs.add(self.sequence_tab, text = "Sequence")

        self.tabs.pack(fill = tk.BOTH, expand=True)

        self.list_text = ListText(self.plate_tab, self.datamodel)
        self.list_text.pack(fill=tk.BOTH,expand=True)

        # self.sfe_sequence_text = SFE_SequenceText(self.sequence_tab, sample_list)
        # self.sfe_sequence_text.pack(fill=tk.BOTH,expand=True)
        return
    
    def refreshProject(self):
        self.list_text.refresh()
        return

class ListText(tk.Text):

    def __init__(self, parent, datamodel):

        self.parent = parent
        self.datamodel= datamodel
        self.scrollbar = tk.Scrollbar(self.parent)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Text.__init__(self, self.parent, yscrollcommand=self.scrollbar.set)  
        self.scrollbar.config(command=self.yview)
        self.buildListText()
        

        return
    
    def buildListText(self):
        self.config(state = 'normal')
        self.delete(1.0, tk.END)
        # if self.datamodel.project_loaded:
        for line in self.datamodel.getSequenceDisplay():
            self.insert(tk.END, str(line))
        self.config(state = 'disabled')

        return
    
    def refresh(self):
        self.buildListText()
        return




class SequenceApp():

    def __init__(self, root):

        self.root_window = root
        self.datamodel = DataModel()
        # self.datamodel.openSampleList("/home/david/IDeA_Scripts/TestData/LiuY_20241205_01_DDA_SampleList.xlsx")
        self.buildUI()

        return

    def buildUI(self):

        self.createMenu()
        
        self.main_frame = tk.Frame(self.root_window, **frame_options)
        self.top_buttons_frame = tk.Frame(self.main_frame, **frame_options)
        self.top_frame = tk.Frame(self.main_frame, **frame_options)
        self.body_frame = tk.Frame(self.main_frame, **frame_options)
        self.left_frame = tk.Frame(self.body_frame, **frame_options)
        self.right_frame = tk.Frame(self.body_frame, **frame_options)
        self.bottom_frame = tk.Frame(self.root_window, **frame_options)

        self.main_frame.pack(side = tk.TOP, fill=tk.BOTH, expand=True)
        self.top_buttons_frame.pack(side=tk.TOP, fill=tk.Y, anchor=tk.W)
        self.top_frame.pack(side = tk.TOP, fill=tk.X, anchor = tk.W)
        self.body_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.left_frame.pack(side = tk.LEFT, anchor=tk.W, fill=tk.BOTH, expand=True)
        self.right_frame.pack(side = tk.RIGHT, anchor=tk.N)
        self.bottom_frame.pack(side = tk.TOP)

        self.head = HeaderFrame(self.top_frame, self.datamodel)
        self.head.pack(side = tk.LEFT, anchor=tk.W)

        self.list_frame = ListFrame(self.left_frame, self.datamodel)
        self.list_frame.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)

        self.option_frame = OptionFrame(self.right_frame, self.datamodel, onStartChange=self.refreshSequence, onRandom=self.onRandom)
        self.option_frame.pack(side=tk.TOP)

        self.instrument_frame = InstrumentFrame(self.top_frame, self.datamodel, self.onInstrumentChange, self.editmenu_edit_methods)
        self.instrument_frame.pack(side=tk.RIGHT, anchor=tk.E)

        self.open_button = tk.Button(self.top_buttons_frame, text="Open Sample List", command=self.filemenu_open)
        self.open_button.pack(side=tk.LEFT, anchor=tk.W)
        

        self.create_button = tk.Button(self.top_buttons_frame, text="Create Sequence", command=self.filemenu_create)
        self.create_button.pack(side=tk.LEFT, anchor=tk.W)
        self.exit_button = tk.Button(self.top_buttons_frame, text = "Exit", command = self.onExit)
        self.exit_button.pack(side=tk.LEFT, anchor=tk.W)

        return
    
    def onExit(self):
        self.root_window.destroy()
        return
    
    def onLoad(self):
        self.option_frame.refreshProject()
        self.refreshSequence()
        
    
    def onCreate(self):

        return
    
    def onInstrumentChange(self):
        self.option_frame.onChange()
        self.refreshSequence()
        return
    
    def onRandom(self):
        self.datamodel.randomize()
        self.refreshSequence()

    def refreshSequence(self):
        self.datamodel.refreshSequence()
        self.list_frame.refreshProject()


    

    ##################################
    ######   Menu
    #################################

    def filemenu_open(self):
        filename = filedialog.askopenfilename(parent=self.root_window, title="Open Sample List", filetypes=(("Excel Files", "*_SampleList.xlsx"),("All Files", "*.*")))
        if filename:
            self.datamodel.openSampleList(filename)
            self.onLoad()
        return
    
    def filemenu_create(self):
        dname = os.path.dirname(self.datamodel.sample_list_path) if self.datamodel.sample_list_path is not None else self.datamodel.settings.default_save_folder
        fname = "{}_Injection_Sequence.csv".format(self.datamodel.project_name)
        filename = filedialog.asksaveasfilename(parent=self.root_window, title="Open Sample List", initialdir=dname, initialfile=fname,filetypes=(("Excel Files", "*_SampleList.xlsx"),("All Files", "*.*")))
        if not filename:
            print ("Cancelled:")
            return
        ###  Pass in sample list file name and sequence builder will replace filename and save next to it. 
        # filename = self.datamodel.sample_list_path_var.get()
        print(filename)
        self.datamodel.onCreateSampleList(filename)
        return
    
    def editmenu_edit_methods(self):
        dlg = EditMethodsDialog(self.root_window, self.datamodel)
        if dlg.result is not None:
            self.datamodel.instrument_data[self.datamodel.getOption('instrument')]['methods'][self.datamodel.getOption('diadda')] = dlg.result
            self.datamodel.save_instrument_data()
            self.instrument_frame.onInstrumentChange()
        return
    
    def editmenu_settings(self):
        dlg = SettingsDialog(self.root_window, self.datamodel)

        return

    
    def createMenu(self):

        self.filemenu_items = {
            'Open':self.filemenu_open,
            'Create_Sequence':self.filemenu_create,
            }
        
        self.editmenu_items = {
            'Edit Methods':self.editmenu_edit_methods,
            'Settings':self.editmenu_settings,
            }

        self.menubar = Menu(self.root_window)

        self.filemenu = Menu(self.menubar, tearoff=0)
        for k,v in self.filemenu_items.items():
            self.filemenu.add_command(label=k, command=v)

        self.editmenu = Menu(self.menubar, tearoff=0)
        for k,v in self.editmenu_items.items():
            self.editmenu.add_command(label=k, command=v)

        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        self.root_window.config(menu=self.menubar)

        return







def startSequenceApp():

    root = tk.Tk()    
    root.geometry("1200x900")
    root.eval('tk::PlaceWindow . center')
    # root.iconbitmap("IDEA_Logo.ico")
    root.title("IDEA Sequence Builder")
    app = SequenceApp(root)
    root.mainloop()


if (__name__ == "__main__"):
    startSequenceApp()

