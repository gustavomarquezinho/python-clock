from tkinter import Canvas

from tkinter.ttk import (
    Button,
    Frame,
    Label,
    Scrollbar,
)

from typing import List, Tuple
from time import time

class Stopwatch:
    def __init__(self, window, frame) -> None:
        self.window = window
        self.frame = frame

        self.timer = None
        self.milliseconds = 0
        self.last_update = 0

        self.was_running = False

        self.leaps_info: List[Tuple[Label, int]] = []
        self.previous_leap = 0

        self.time_label = None
        self.leaps_header = None
        self.start_button = None
        self.reset_button = None
        self.leaps_view = None

        self.create()

    def create(self):
        self.time_label = Label(
            self.frame,
            text='00:00:00.00',
            font=('Poppins ExtraLight', 56)
        )

        self.leaps_header = Label(
            self.frame,
            text='\n',
            font=('Gadugi', 12),
            foreground='#6A6A6B',
            justify='center'
        )

        self.start_button = Button(
            self.frame,
            text='Iniciar',
            width=16,
            command=lambda: self.start() if self.timer is None else self.stop()
        )

        self.reset_button = Button(
            self.frame,
            text='Reiniciar',
            width=16,
            command=lambda: self.reset() if self.timer is None else self.leap()
        )

    def show(self):
        self.time_label.grid(row=0, pady=(0, 10))
        self.leaps_header.grid(row=1)

        self.start_button.grid(row=3, padx=(0, 200), pady=(20 + 100, 0), ipady=8)
        self.reset_button.grid(row=3, padx=(200, 0), pady=(20 + 100, 0), ipady=8)

        if self.was_running and self.timer is None:
            self.update(repeat=True)

    def hide(self):
        self.time_label.grid_forget()
        self.leaps_header.grid_forget()
        self.start_button.grid_forget()
        self.reset_button.grid_forget()

        if self.leaps_view is not None and self.leaps_view.winfo_exists():
            self.leaps_view.destroy()

        self.was_running = False

        if self.timer is not None:
            self.window.after_cancel(self.timer)
            self.timer = None

            self.was_running = True

    def start(self):
        self.start_button['text'] = 'Pausar'
        self.reset_button['text'] = 'Volta'

        self.last_update = round(time() * 1000)
        self.update(repeat=True)

    def stop(self):
        self.start_button['text'] = 'Continuar'
        self.reset_button['text'] = 'Reiniciar'

        self.window.after_cancel(self.timer)
        self.timer = None

        self.update(repeat=False)

    def reset(self):
        self.time_label['text'] = '00:00:00.00'

        self.leaps_header['text'] = '\n'

        if self.leaps_view is not None and self.leaps_view.winfo_exists():
            self.leaps_view.destroy()

        self.start_button['text'] = 'Iniciar'
        self.start_button.grid_configure(pady=(120, 0))

        self.reset_button['text'] = 'Reiniciar'
        self.reset_button.grid_configure(pady=(120, 0))

        self.milliseconds = 0

        self.leaps_info.clear()
        self.previous_leap = 0

    def leap(self):
        length = len(self.leaps_info)

        if self.leaps_view is None or not self.leaps_view.winfo_exists():
            self.leaps_view = LeapsView(self.frame)

        if not length:
            header = f'{"Volta":<11} {"Tempo das voltas":<22} {"Tempo geral":<18}'
            self.leaps_header['text'] = f'{header:>60}\n' + ('_' * len(header))

            self.leaps_view.grid(row=2, pady=(10, 0))

            self.start_button.grid_configure(pady=(16, 0))
            self.reset_button.grid_configure(pady=(16, 0))

        formatted_leap_time = self.get_formatted_time(self.milliseconds - self.previous_leap)
        text = f'{str(length + 1).zfill(2)} {formatted_leap_time:>26} {self.time_label["text"]:>23}'
        text = f'{str(length).zfill(2):^20} {formatted_leap_time:^20} {self.time_label["text"]:^20}'

        label = Label(
            self.leaps_view.frame,
            text=f'{text:>64}',
            font=('Gadugi', 12),
            justify='center'
        )
        label.grid()

        self.leaps_info.append((label, self.milliseconds - self.previous_leap))
        self.previous_leap = self.milliseconds

        if length > 2:
            self.highlight_leaps()

    def highlight_leaps(self):
        leaps = [leap[1] for leap in self.leaps_info]

        best_leap_index = leaps.index(min(leaps))
        worst_leap_index = leaps.index(max(leaps))

        for index, info in enumerate(self.leaps_info):
            label = info[0]

            if index == best_leap_index:
                label['foreground'] = '#0dbd2d'
            elif index == worst_leap_index:
                label['foreground'] = '#ff0000'
            else:
                label['foreground'] = '#000000'

    def update(self, repeat: bool):
        current_time = round(time() * 1000)

        self.milliseconds += (current_time - self.last_update)
        self.last_update = current_time

        self.time_label['text'] = self.get_formatted_time(self.milliseconds)

        if repeat:
            self.timer = self.window.after(20, lambda: self.update(repeat=True))

    @staticmethod
    def get_formatted_time(milliseconds: int) -> str:
        hours = milliseconds // 1000 // 60 // 60
        milliseconds -= hours * 1000 * 60 * 60

        minutes = milliseconds // 1000 // 60
        milliseconds -= minutes * 1000 * 60

        seconds = milliseconds // 1000 % 60
        milliseconds -= seconds * 1000

        return f'{hours:02}:{minutes:02}:{seconds:02}.{str(round(milliseconds)).zfill(3)[:2]}'


class LeapsView(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.canvas = None
        self.frame = None
        self.scrollbar = None

        self.create()
        self.layout()

    def create(self):
        self.canvas = Canvas(
            self,
            borderwidth=0,
            background='#fafafa',
            height=90,
            width=360,
        )

        self.frame = Frame(self.canvas)

        self.canvas.create_window(
            (4, 4),
            window=self.frame,
            tags='self.frame',
            anchor='s'
        )

        self.scrollbar = Scrollbar(
            self,
            orient='vertical',
            command=self.canvas.yview,
        )

        self.frame.bind('<Configure>', self.on_frame_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

    def layout(self):
        self.canvas.pack(side='left', fill='both', anchor='nw')
        self.scrollbar.pack(side='left', fill='y')

    def on_frame_configure(self, _):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
