from tkinter import *
from mods import tables, GlobStat, ByAllStats, FPages


class ScrollableFrame(Frame):
    def __init__(self, parent, *args, **kw):
        '''
        Constructor
        '''

        Frame.__init__(self, parent, *args, **kw)

        # create a vertical scrollbar
        vscrollbar = Scrollbar(self, orient = VERTICAL)
        vscrollbar.pack(fill = Y, side = RIGHT, expand = FALSE)

        # create a horizontal scrollbar
        hscrollbar = Scrollbar(self, orient = HORIZONTAL)
        hscrollbar.pack(fill = X, side = BOTTOM, expand = FALSE)

        #Create a canvas object and associate the scrollbars with it
        self.canvas = Canvas(self, bd = 0, highlightthickness = 0, yscrollcommand = vscrollbar.set, xscrollcommand = hscrollbar.set)
        self.canvas.pack(side = LEFT, fill = BOTH, expand = TRUE)

        #Associate scrollbars with canvas view
        vscrollbar.config(command = self.canvas.yview)
        hscrollbar.config(command = self.canvas.xview)


        # set the view to 0,0 at initialization

        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create an interior frame to be created inside the canvas

        self.interior = interior = Frame(self.canvas)
        interior_id = self.canvas.create_window(0, 0, window=interior,
                anchor=NW, width=700)


        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar

        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            print(size)
            self.canvas.config(scrollregion='0 0 %s %s' % size)
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                self.canvas.config(width = interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)



podContQuests = {}
qVariants = {}
statsQuests = []
def resize(event):
    pass

class Window:
    def __init__(self, type, name='', parentrt=None):
        global podContQuests
        x = 0
        y = 0
        self.type = type
        self.name = name
        self.root = Tk()
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.resizable(False, True)
        self.root.title(name if type != 'main' else "Категории вопросов")
        rgeo = f"{600}x{320}+{400}+{250}"
        self.width = 600
        self.height = 320
        self.root.geometry(rgeo)

        if type != 'main':
            parentrt.withdraw()

        frame = ScrollableFrame(self.root)
        frame.grid(column=x, row=y, sticky='EWSN')
        frame.grid_columnconfigure(0, weight=1)

        if type != 'main':
            Label(frame.interior, text='Название').grid(column=x, row=y)
            x += 1
            self.entry = Entry(frame.interior)
            self.entry.grid(column=x, row=y, columnspan=2)
            self.entry.insert(0, self.name)
            y += 1
            x = 0

        Label(frame.interior, text='Вопросы' if type != 'main' else 'Категории').grid(column=x, row=y)
        y += 1
        names = []
        if type != 'main' and tables is not None:
            names = [i for i in tables]
        else:
            names = [i for i in podContQuests]
        self.var = Variable(frame.interior, value=names)
        self.listbox = Listbox(frame.interior, listvariable=self.var, height=10)
        self.listbox.grid(column=x, row=y, columnspan=3, sticky="EW")
        x += 3
        scrollbar = Scrollbar(frame.interior)
        scrollbar.grid(column=x, row=y, sticky=NS)
        y += 1
        x = 0
        self.listbox.config(yscrollcommand=scrollbar.set, selectmode=SINGLE)
        scrollbar.config(command=self.listbox.yview)
        if type != 'main':
            self.listbox.bind('<<ListboxSelect>>', lambda e: self.Select(type='listbox'))
            Button(frame.interior, text='Назад', command=lambda: self.Back()).grid(column=x, row=y)
            y += 1
            x = 0
            Label(frame.interior, text='Добавление варианта').grid(column=x, row=y)
            x += 1
            self.qName = Entry(frame.interior)
            self.qName.grid(column=x, row=y)
            x = 0
            y+=1
            Button(frame.interior, text='Добавить', command=lambda: self.Add()).grid(column=x, row=y)
            x+=1
            Button(frame.interior, text='Удалить', command=lambda: self.Delete()).grid(column=x, row=y)
            x = 0
            y += 1
            names = []
            if qVariants.get(self.name) is not None:
                names = [i for i in qVariants[self.name]['values']]
            self.variantsVar = Variable(frame.interior, value=names)
            self.variants = Listbox(frame.interior, listvariable=self.variantsVar, width=92, height=10)
            self.variants.grid(column=x, row=y, columnspan=3)
            x += 3
            scrollbar = Scrollbar(frame.interior)
            scrollbar.grid(column=x, row=y, sticky=NS)
            y += 1
            x = 0
            self.variants.config(yscrollcommand=scrollbar.set, selectmode=SINGLE)
            scrollbar.config(command=self.variants.yview)
            self.variants.bind('<<ListboxSelect>>', lambda e: self.DoubleSelect())
            self.CheckListbox()

            Label(frame.interior, text='Тип формулы').grid(column=x, row=y)
            y += 1
            self.ansType = BooleanVar(frame.interior)
            self.ansType.set(qVariants[self.name]['type'])
            Radiobutton(frame.interior, text='Положительные', variable=self.ansType, value=True).grid(column=x,row=y)
            x += 1
            Radiobutton(frame.interior, text='Положительные - отрицательные', variable=self.ansType,value=False).grid(column=x, row=y)
            y += 1
            x = 0
        else:
            Button(frame.interior, text='Добавить', command=lambda: self.Add()).grid(column=x, row=y)
            x += 1
            Button(frame.interior, text='Изменить', command=lambda: self.Select('listbox')).grid(column=x,row=y)
            x += 1
            Button(frame.interior, text='Сохранить', command=lambda: self.Save()).grid(column=x, row=y)
            y += 1
            x = 0
            Button(frame.interior, text='Удалить', command=lambda: self.Delete()).grid(column=x, row=y)
            y+=1
            Label(frame.interior, text='Вопросы статистики').grid(column=x, row=y)
            y += 1
            names = [i for i in tables]
            namesVar = Variable(frame.interior, value=names)
            self.allStat = Listbox(frame.interior, listvariable=namesVar, width=92, height=10)
            self.allStat.grid(column=x, row=y, columnspan=3)
            x += 3
            scrollbar = Scrollbar(frame.interior)
            scrollbar.grid(column=x, row=y, sticky=NS)
            y += 1
            x = 0
            self.allStat.config(yscrollcommand=scrollbar.set, selectmode=SINGLE)
            scrollbar.config(command=self.allStat.yview)
            self.allStat.bind('<<ListboxSelect>>', lambda e: self.Select(type='allStat'))
            self.CheckListbox()
        self.root.bind("<Configure>", resize)

    def Delete(self):
        if self.type == 'cat' and qVariants.get(self.name) is not None and len(qVariants[self.name]['values']) != 0:
            try:
                value = self.variants.get(self.variants.curselection()[0])
                del qVariants[self.name]['values'][value]
                self.variantsVar.set([i for i in qVariants[self.name]['values']])
            except:
                pass
        elif self.type == 'main' and len(podContQuests) != 0:
            value = self.listbox.get(self.listbox.curselection()[0])
            del podContQuests[value]
            self.var.set([i for i in podContQuests])
        Save()

    def DoubleSelect(self):
        if self.type == 'cat':
            try:
                value = self.variants.get(self.variants.curselection()[0])
                if qVariants[self.name]['values'][value] == 'green':
                    self.variants.itemconfig(self.variants.curselection()[0], {'bg': 'red'})
                    qVariants[self.name]['values'][value] = 'red'
                else:
                    self.variants.itemconfig(self.variants.curselection()[0], {'bg': 'green'})
                    qVariants[self.name]['values'][value] = 'green'
            except:
                pass

    def CheckListbox(self):
        if self.type == 'cat':
            for quest in podContQuests[self.name]:
                try:
                    self.listbox.itemconfig(self.listbox.get(0, "end").index(quest), {'bg': 'green'})
                except:
                    podContQuests[self.name].remove(quest)
            for variant in qVariants[self.name]['values']:
                try:
                    if len(qVariants[self.name]['values'][variant]) != 0:
                        if qVariants[self.name]['values'][variant] == 'green':
                            self.variants.itemconfig(self.variants.get(0, "end").index(variant), {'bg': 'green'})
                        else:
                            self.variants.itemconfig(self.variants.get(0, "end").index(variant), {'bg': 'red'})
                except:
                    qVariants[self.name]['values'].remove(variant)

        else:
            for quest in statsQuests:
                try:
                    self.allStat.itemconfig(self.allStat.get(0, "end").index(quest), {'bg': 'green'})
                except:
                    statsQuests.remove(quest)

    def Select(self, type):
        if self.type == 'main' and type == 'listbox':
            Window(type='cat', name=self.listbox.get(self.listbox.curselection()[0]), parentrt=self.root)
        else:
            try:
                value = eval(f'self.{type}.get(self.{type}.curselection()[0])')
                if value in (podContQuests[self.name] if type == 'listbox' else statsQuests):
                    exec(f'self.{type}.itemconfig(self.{type}.curselection()[0], {{"bg": "white"}})')
                    exec(f'{"podContQuests[self.name]" if type == "listbox" else "statsQuests"}.remove(value)')
                else:
                    exec(f'self.{type}.itemconfig(self.{type}.curselection()[0], {{"bg": "green"}})')
                    exec(f'{"podContQuests[self.name]" if type == "listbox" else "statsQuests"}.append(value)')
                Save()
            except:
                pass

    def Save(self):
        if self.type == 'main':
            GlobStat(podContQuests, qVariants)
            ByAllStats(statsQuests, qVariants)
            # FPages()

    def Back(self):
        if self.type == 'cat':
            qVariants[self.name]['type'] = self.ansType.get()
            if self.name != self.entry.get() and podContQuests.get(self.entry.get()) is None:
                podContQuests[self.entry.get() if self.entry.get() != '' else 'Новая категория'] = podContQuests[
                    self.name]
                qVariants[self.entry.get() if self.entry.get() != '' else 'Новая категория'] = qVariants[self.name]
                del podContQuests[self.name]
                del qVariants[self.name]
            elif self.name != self.entry.get():
                return 0
            self.root.destroy()
            global main
            main.cat = None
            main.root.deiconify()
            main.var.set([i for i in podContQuests])
            Save()

    def Add(self):
        if self.type == 'main' and podContQuests.get('Новая категория') is None:
            podContQuests['Новая категория'] = []
            qVariants['Новая категория'] = {'type': True, 'values': {}}
            Window(type='cat', name='Новая категория', parentrt=self.root)
            self.var.set([i for i in podContQuests])
        elif self.type == 'cat':
            qVariants[self.name]['values'][self.qName.get().lower()] = 'green'
            self.variantsVar.set([i for i in qVariants[self.name]['values']])
            self.CheckListbox()
        Save()

def Save():
    with open('./saves.txt', 'w', encoding='UTF-8') as f:
        global podContQuests, statsQuests
        f.write(str({'pod': podContQuests, 'stat': statsQuests, 'vars': qVariants}))

def LoadSaves():
    with open('./saves.txt', 'r', encoding='UTF-8') as f:
        global podContQuests, statsQuests, qVariants
        ans = eval(f.read())
        if len(ans) != 0:
            try:
                podContQuests = ans['pod']
            except:
                pass
            try:
                statsQuests = ans['stat']
            except:
                pass
            try:
                qVariants = ans['vars']
            except:
                pass


LoadSaves()
main = Window('main')
