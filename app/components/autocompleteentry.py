from tkinter import *
from ..utility import settings

class AutocompleteEntry(Entry):
    def __init__(self, lista, parent, *args, **kwargs):
        self.allow_selection = kwargs.pop('allow_selection', True)
        self.when_selected = kwargs.pop('when_selected', None)
        Entry.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.lista = lista       
        self.var = kwargs["textvariable"]

        self.traceid = self.var.trace('w', self.changed)
        #self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)

        self.bind("<Tab>", self.close)
        self.bind("<Return>", self.close)  # <Return> represents the Enter key
        self.bind("<Escape>", self.close)
        #self.bind("<FocusOut>", self.close)
        
        self.lb_up = False
        self.selected = None

    def set_variable(self, newVal):
        self.var.trace_remove('write', self.traceid)
        self.var.set(newVal)
        self.traceid = self.var.trace('w', self.changed)
        if self.selected is not None:
            self.config(bg=self.get_id_color())

    def changed(self, name, index, mode):
        self.selected = None
        self.config(bg='white')
        if self.var.get() == '':
            if hasattr(self, 'lb'):
                self.lb.destroy()
            self.lb_up = False
        else:
            self.lista = self.comparison()
            words = self.lista
            if words:            
                if not self.lb_up:
                    self.lb = Listbox(self.parent)
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)

                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height(), width=250)

                    self.lb_up = True
                
                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END,w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False
        
    def selection(self, event):
        if self.lb_up and self.allow_selection:
            #selected = self.lb.get(ACTIVE)
            selected = self.lb.curselection()[0]
            selected = self.lista[selected]
            self.var.set(selected)
            self.selected = selected
            self.config(bg=self.get_id_color())
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)
            if self.when_selected:
                self.when_selected(selected)

    def close(self, event):
        if self.lb_up:
            self.lb.destroy()
            self.lb_up = False

    def up(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':                
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)                
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def down(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:                        
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)        
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def comparison(self):
        return self.lista
#        pattern = re.compile('.*' + self.var.get() + '.*')
#        return [w for w in self.lista if re.match(pattern, w)]

    def get_id_color(self):
        return settings.config['colors']['neutral standing']