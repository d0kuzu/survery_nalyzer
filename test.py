from tkinter import *


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
        self.canvas = Canvas(self, bg='green', bd = 0, highlightthickness = 0, yscrollcommand = vscrollbar.set, xscrollcommand = hscrollbar.set)
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
                anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar

        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            self.canvas.config(scrollregion='0 0 %s %s' % size)
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                self.canvas.config(width = interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)


class my_gui():

    def __init__(self):
        self.root = Tk()

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.frame = ScrollableFrame(self.root)
        self.frame.grid(sticky='EWSN')

        self.__add_plot()

    def __add_plot(self):
        # create a rectangle
        [Label(self.frame.interior, text='sui').grid() for i in range(100)]

    def mainLoop(self):
        # This function starts an endlos running thread through the gui
        self.root.mainloop()

    def __quit(self):
        # close everything
        self.root.quit()


# init gui
my_gui = my_gui()
# execute gui
my_gui.mainLoop()