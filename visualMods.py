from tkinter import *
from mods import contQuests, podContQuests, tables


class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self, width=577)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class Window:
    def __init__(self, name='', id=''):
        x = 0
        y = 0
        # if type != 'cats':
        #     parentrt.withdraw()
        self.root = Tk()
        self.root.title('Настройки')
        rgeo = f"{600}x{320}+{400}+{250}"
        self.root.geometry(rgeo)

        frame = ScrollableFrame(self.root)
        frame.grid(column=x, row=y)

        # contQuests
        Label(frame.scrollable_frame, text='Вопросы').grid(column=x, row=y)
        y += 1
        names = []
        if tables is not None:
            [names.append(i) for i in tables]
        namesVar = Variable(frame.scrollable_frame, value=names)
        self.listbox = Listbox(frame.scrollable_frame, listvariable=namesVar, width=93, height=10)
        self.listbox.grid(column=x, row=y, columnspan=2)
        x += 2
        scrollbar = Scrollbar(frame.scrollable_frame)
        scrollbar.grid(column=x, row=y, sticky=NS)
        y += 1
        x = 0
        self.listbox.config(yscrollcommand=scrollbar.set, selectmode=SINGLE)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.bind('<<ListboxSelect>>', lambda e: self.Change(self.listbox))
        self.CheckForSaves(isCont=True)
        # vov
        self.contVar = Variable(frame.scrollable_frame, value=contQuests)
        Label(frame.scrollable_frame, text='Вовлечённость').grid(column=x, row=y)
        y += 1
        self.vov = Listbox(frame.scrollable_frame, listvariable=self.contVar, width=93, height=10)
        self.vov.grid(column=x, row=y, columnspan=2)
        x += 2
        scrollbar = Scrollbar(frame.scrollable_frame)
        scrollbar.grid(column=x, row=y, sticky=NS)
        y += 1
        x = 0
        self.vov.config(yscrollcommand=scrollbar.set, selectmode=SINGLE)
        scrollbar.config(command=self.vov.yview)
        self.vov.bind('<<ListboxSelect>>', lambda e: self.Change(self.vov, 'vov'))
        # vzaim
        self.contVar = Variable(frame.scrollable_frame, value=contQuests)
        Label(frame.scrollable_frame, text='Взаимоотношение').grid(column=x, row=y)
        y += 1
        self.vzaim = Listbox(frame.scrollable_frame, listvariable=self.contVar, width=93, height=10)
        self.vzaim.grid(column=x, row=y, columnspan=2)
        x += 2
        scrollbar = Scrollbar(frame.scrollable_frame)
        scrollbar.grid(column=x, row=y, sticky=NS)
        y += 1
        x = 0
        self.vzaim.config(yscrollcommand=scrollbar.set, selectmode=SINGLE)
        scrollbar.config(command=self.vzaim.yview)
        self.vzaim.bind('<<ListboxSelect>>', lambda e: self.Change(self.vzaim, 'vzaim'))
        # razv
        self.contVar = Variable(frame.scrollable_frame, value=contQuests)
        Label(frame.scrollable_frame, text='Развитие').grid(column=x, row=y)
        y += 1
        self.razv = Listbox(frame.scrollable_frame, listvariable=self.contVar, width=93, height=10)
        self.razv.grid(column=x, row=y, columnspan=2)
        x += 2
        scrollbar = Scrollbar(frame.scrollable_frame)
        scrollbar.grid(column=x, row=y, sticky=NS)
        y += 1
        x = 0
        self.razv.config(yscrollcommand=scrollbar.set, selectmode=SINGLE)
        scrollbar.config(command=self.razv.yview)
        self.razv.bind('<<ListboxSelect>>', lambda e: self.Change(self.razv, 'razv'))
        # priv
        self.contVar = Variable(frame.scrollable_frame, value=contQuests)
        Label(frame.scrollable_frame, text='Приверженность').grid(column=x, row=y)
        y += 1
        self.priv = Listbox(frame.scrollable_frame, listvariable=self.contVar, width=93, height=10)
        self.priv.grid(column=x, row=y, columnspan=2)
        x += 2
        scrollbar = Scrollbar(frame.scrollable_frame)
        scrollbar.grid(column=x, row=y, sticky=NS)
        y += 1
        x = 0
        self.priv.config(yscrollcommand=scrollbar.set, selectmode=SINGLE)
        scrollbar.config(command=self.priv.yview)
        self.priv.bind('<<ListboxSelect>>', lambda e: self.Change(self.priv, 'priv'))
        # udov
        self.contVar = Variable(frame.scrollable_frame, value=contQuests)
        Label(frame.scrollable_frame, text='Удовлетворенность').grid(column=x, row=y)
        y += 1
        self.udov = Listbox(frame.scrollable_frame, listvariable=self.contVar, width=93, height=10)
        self.udov.grid(column=x, row=y, columnspan=2)
        x += 2
        scrollbar = Scrollbar(frame.scrollable_frame)
        scrollbar.grid(column=x, row=y, sticky=NS)
        y += 1
        x = 0
        self.udov.config(yscrollcommand=scrollbar.set, selectmode=SINGLE)
        scrollbar.config(command=self.udov.yview)
        self.udov.bind('<<ListboxSelect>>', lambda e: self.Change(self.udov, 'udov'))

        self.CheckForSaves()

    def CheckForSaves(self, isCont=False):
        global contQuests
        ans = None
        with open('./saves.txt', 'r', encoding='UTF-8') as f:
            ans = eval(f.read())

        if isCont and ans.get('contQuests') is not None:
            contQuests = ans['contQuests']
            for quest in contQuests:
                try:
                    self.listbox.itemconfig(self.listbox.get(0, "end").index(quest), {'bg': 'green'})
                except:
                    contQuests.remove(quest)
        elif not isCont:
            for i in podContQuests:
                if ans.get(i) is not None:
                    podContQuests[i] = ans[i]
                    for quest in podContQuests[i]:
                        try:
                            exec(f"self.{i}.itemconfig(self.{i}.get(0, 'end').index('{quest}'), {{'bg': 'green'}})")
                        except:
                            podContQuests[i].remove(quest)

    def Change(self, listbox, type='contQuests'):
        try:
            value = listbox.get(listbox.curselection()[0])
            if value in (contQuests if type == 'contQuests' else podContQuests['vov']):
                listbox.itemconfig(listbox.curselection()[0], {'bg': 'white'})
                try:
                    contQuests.remove(value) if type == 'contQuests' else podContQuests['vov'].remove(value)
                except:
                    pass
            else:
                listbox.itemconfig(listbox.curselection()[0], {'bg': 'green'})
                try:
                    contQuests.append(value) if type == 'contQuests' else podContQuests['vov'].append(value)
                except:
                    pass
            with open('./saves.txt', 'w', encoding='UTF-8') as f:
                f.write(str({'contQuests': contQuests} | podContQuests))
            self.contVar.set(contQuests)
        except:
            pass
