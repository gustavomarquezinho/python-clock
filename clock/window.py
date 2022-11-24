from tkinter import (
    Frame,
    PhotoImage,
    Tk,
)

from tkinter.ttk import (
    Notebook,
    Style
)


class Window(Tk):
    tabs = (
        'Horário',
        'Cronômetro',
        'Alarme',
        'Temporizador'
    )

    def __init__(self):
        super().__init__()

        self.width = 600

        self.create_window(self.width, 400)
        self.stylize_window()

        self.current_tab = None

        self.frame = Frame(pady=25)
        self.frame.grid(row=1)

        self.create_tabs(self.tabs)

    def create_window(self, size_x, size_y):
        screen_x = self.winfo_screenwidth()
        screen_y = self.winfo_screenheight()

        center_x = int((screen_x / 2) - (size_x / 2))
        center_y = int((screen_y / 2) - (size_y / 2))

        self.geometry(f'{size_x}x{size_y}+{center_x}+{center_y}')

        self.title('Python Clock')
        self.resizable(0, 0)

    def stylize_window(self):
        self.tk.call('source', './clock/assets/Sun Valley/sun-valley.tcl')
        self.tk.call('set_theme', 'light')

        Style().configure('Tab', focuscolor=Style().configure('.')['background'])

        self.iconphoto(False, PhotoImage(file='./clock/assets/icon_small.png', master=self))

    def create_tabs(self, titles: tuple):
        self.notebook = Notebook()
        self.notebook.grid(row=0)

        for title in titles:
            frame = Frame(width=self.width)
            frame.grid(row=0)

            self.notebook.add(frame, text=f'{title:^22}')

        self.notebook.bind('<<NotebookTabChanged>>', lambda e: self.switch_tab())

    def switch_tab(self):
        self.current_tab = self.tabs[self.notebook.index('current')]


if __name__ == '__main__':
    gui = Window()
    gui.mainloop()
