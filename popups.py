import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import openpyxl
from datamodel import DataModel

#################################################################
#############################################################
#####    Helper to keep popups centered and looking nice
#############################################################
#################################################################


def show_modal_centered(win: tk.Toplevel, master: tk.Misc, *, topmost_pulse: bool = True) -> None:
    """
    Make a Toplevel modal, raise it above the parent, and center it over the parent.
    Call this after you've created and laid out the dialog's widgets.
    """
    # Tie to parent and make modal
    win.withdraw()
    win.transient(master)
    try:
        win.grab_set()
    except tk.TclError:
        pass  # safe fallback if grabs aren't allowed in some contexts

    # Ensure sizes are computed

    master.update_idletasks()

    # Compute target rect (parent if mapped, else screen)
    try:
        parent_is_visible = bool(master.winfo_viewable())
    except tk.TclError:
        parent_is_visible = False

    if parent_is_visible:
        px, py = master.winfo_rootx(), master.winfo_rooty()
        pw, ph = master.winfo_width(), master.winfo_height()
    else:
        px, py = 0, 0
        pw, ph = win.winfo_screenwidth(), win.winfo_screenheight()

    win.update_idletasks()
    ww, wh = win.winfo_reqwidth(), win.winfo_reqheight()
    x = px + max(0, (pw - ww) // 2)
    y = py + max(0, (ph - wh) // 2)

    # Clamp to screen so it never spawns off-screen
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    x = max(0, min(x, sw - ww))
    y = max(0, min(y, sh - wh))

    win.geometry(f"+{x}+{y}")
    win.deiconify()
    win.lift()
    if topmost_pulse:
        # Briefly set topmost to ensure it’s in front, then release (avoids sticking above everything forever)
        win.attributes("-topmost", True)
        win.after(50, lambda: win.attributes("-topmost", False))

    # Focus it
    try:
        win.focus_force()
    except tk.TclError:
        pass


class EditMethodsDialog(tk.Toplevel):
    def __init__(self, parent: tk.Misc, datamodel: DataModel):
        super().__init__(parent)
        self.parent = parent
        self.datamodel = datamodel
        self.title("Edit Method List")

        self.result = None  # Will hold the updated list of methods or None if cancelled

        ###  A list of the methods available for the selected instrument
        self.methods = self.datamodel.getInstrumentData('methods')[self.datamodel.getOption('diadda')]

        self.methodsVar = tk.StringVar(value=self.methods)

        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.listFrame = tk.Frame(self.container)
        self.listFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.buttonFrame = tk.Frame(self.container)
        self.buttonFrame.pack(side=tk.LEFT, fill=tk.Y)

        self.listbox = tk.Listbox(self.listFrame, listvariable=self.methodsVar, selectmode=tk.SINGLE, height=10, width=50)
        self.listbox.pack()

        self.addButton = tk.Button(self.buttonFrame, text="Add", command=self.addMethod)
        self.addButton.pack(fill=tk.X)

        self.removeButton = tk.Button(self.buttonFrame, text="Remove", command=self.removeMethod)
        self.removeButton.pack(fill=tk.X)  

        self.upButton = tk.Button(self.buttonFrame, text="Up", command=self.moveUp)
        self.upButton.pack(fill=tk.X)

        self.downButton = tk.Button(self.buttonFrame, text="Down", command=self.moveDown)
        self.downButton.pack(fill=tk.X)      

        self.doneButton = tk.Button(self.buttonFrame, text="Done", command=self.onDone)
        self.doneButton.pack(fill=tk.X) 

        self.cancelButton = tk.Button(self.buttonFrame, text="Cancel", command=self.onCancel)
        self.cancelButton.pack(fill=tk.X)   

        show_modal_centered(self, parent)
        self.wait_window()

        return
    
    def addMethod(self):
        method_path = filedialog.askopenfilename(parent=self, title="Select Method File", filetypes=[("Method Files", "*.meth"), ("All Files", "*.*")])
        if method_path:
            self.methods.append(method_path)
            self.methodsVar.set(self.methods)
        return
    
    def removeMethod(self):
        sel = self.listbox.curselection()
        if sel:
            index = sel[0]
            del self.methods[index]
            self.methodsVar.set(self.methods)
        return
    
    def moveUp(self):
        sel = self.listbox.curselection()
        if sel:
            index = sel[0]
            if index > 0:
                self.methods[index], self.methods[index - 1] = self.methods[index - 1], self.methods[index]
                self.methodsVar.set(self.methods)
                self.listbox.selection_set(index - 1)
        return  
    
    def moveDown(self):
        sel = self.listbox.curselection()
        if sel:
            index = sel[0]
            if index < len(self.methods) - 1:
                self.methods[index], self.methods[index + 1] = self.methods[index + 1], self.methods[index]
                self.methodsVar.set(self.methods)
                self.listbox.selection_set(index + 1)
        return  
    
    def onDone(self):
        self.result = self.methods
        self.destroy()
        return
    
    def onCancel(self):
        self.result = None
        self.destroy()
        return



#########
        ##   Old Exception Handlers from the old version for dealing with Sample List issues


# class AskHeaderRow(tk.Toplevel):

#     def __init__(self, parent, sh):

#         self.parent = parent
#         tk.Toplevel.__init__(self, self.parent)

#         self.sh = sh

#         self.choice = tk.StringVar(value="None")

#         self.top_frame = tk.Frame(self)
#         self.label = tk.Label(self.top_frame, text="Could not find header row.\n  Please select the header for sample number.")
#         self.label.pack()
#         self.top_frame.pack()

#         self.row_frame = tk.Frame(self)
#         self.row_frame.pack()

#         self.button_frame = tk.Frame(self)
#         self.button_frame.pack()

#         self.row = 0

#         self.displayRow()

#         self.done_button = tk.Button(self.button_frame, text="Done", command=self.onDone)
#         self.done_button.pack(side=tk.LEFT)
#         self.next_button = tk.Button(self.button_frame, text="Next Row", command=self.displayRow)
#         self.next_button.pack(side=tk.LEFT)

#         self.parent.eval(f'tk::PlaceWindow {str(self)} center')
#         self.transient(self.parent)
#         self.grab_set()
#         self.parent.wait_window(self)

#         return

#     def onDone(self):
#         self.destroy()

#     def displayRow(self):
#         for w in self.row_frame.winfo_children():
#             w.destroy()
#         self.row += 1

#         for i in range(1, self.sh.max_column + 1):
#             name = self.sh.cell(row = self.row, column = i).value
#             rad = tk.Radiobutton(self.row_frame, text=name, var=self.choice, value=name)
#             rad.pack()


# class askNameColumn(tk.Toplevel):

#     def __init__(self, parent, sh, row):

#         self.parent = parent
#         tk.Toplevel.__init__(self, self.parent)

#         self.sh = sh

#         self.choice = tk.StringVar(value="None")

#         self.top_frame = tk.Frame(self)
#         self.label = tk.Label(self.top_frame, text="Please select header for Sample Name")
#         self.label.pack()
#         self.top_frame.pack()

#         self.row_frame = tk.Frame(self)
#         self.row_frame.pack()

#         self.button_frame = tk.Frame(self)
#         self.button_frame.pack()

#         self.row = row

#         self.displayRow()

#         self.done_button = tk.Button(self.button_frame, text="Done", command=self.onDone)
#         self.done_button.pack(side=tk.LEFT)

#         self.parent.eval(f'tk::PlaceWindow {str(self)} center')
#         self.transient(self.parent)
#         self.grab_set()
#         self.parent.wait_window(self)

#         return

#     def onDone(self):
#         self.destroy()

#     def displayRow(self):

#         for i in range(1, self.sh.max_column + 1):
#             name = self.sh.cell(row = self.row, column = i).value
#             rad = tk.Radiobutton(self.row_frame, text=name, var=self.choice, value=name)
#             rad.pack()




# class AskProjName(tk.Toplevel):

#     def __init__(self, parent):
#         self.parent = parent
#         tk.Toplevel.__init__(self, self.parent)

#         self.frame = tk.Frame(self)

#         self.label = tk.Label(self.frame, text="Please Enter a Project Name")
#         self.label.pack()

#         self.entry = tk.Entry(self.frame, width=50)
#         self.entry.pack()

#         self.button = tk.Button(self.frame, text="OK", command=self.onOk)
#         self.button.pack()


#         self.frame.pack()

#         self.parent.eval(f'tk::PlaceWindow {str(self)} center')
#         self.transient(self.parent)
#         self.grab_set()
#         self.parent.wait_window(self)

#         return

#     def onOk(self):
#         self.result = self.entry.get()
#         self.destroy()