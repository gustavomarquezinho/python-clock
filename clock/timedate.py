from tkinter.ttk import (
    Combobox,
    Label
)

from datetime import datetime
from pytz import timezone


class TimeDate():
    zones = {
        'Brazil': 'Brazil/East',
        'Japan': 'Japan'
    }

    def __init__(self, window, frame):
        super().__init__()

        self.window = window
        self.frame = frame

        self.zone = 'Brazil'

        self.update_timer = None
        self.create()

    def get_time(self):
        return datetime.now(timezone(self.zones[self.zone])).strftime("%H:%M:%S")

    def get_date(self):
        return datetime.now(timezone(self.zones[self.zone])).strftime("%B %d, %Y").title()

    def create(self):
        self.country_label = Label(
            self.frame,
            text='Country',
            font=('Poppins Light', 18)
        )

        self.time_label = Label(
            self.frame,
            text='00:00:00',
            font=('Poppins ExtraLight', 56)
        )

        self.date_label = Label(
            self.frame,
            text='00/00/0000',
            font=('Poppins Light', 18)
        )

        self.countries_label = Combobox(
            values=tuple(self.zones.keys()),
            justify='center',
            state='readonly'
        )

        self.countries_label.set(tuple(self.zones.keys())[0])
        self.countries_label.bind("<<ComboboxSelected>>", lambda e: self.change_country())

    def show(self):
        self.country_label.grid(row=0)
        self.time_label.grid(row=1, pady=(0, 10))
        self.date_label.grid(row=1, pady=(110, 10))
        self.countries_label.grid(ipady=6)

        self.update()

    def hide(self):
        self.country_label.grid_forget()
        self.time_label.grid_forget()
        self.date_label.grid_forget()
        self.countries_label.grid_forget()

        self.window.after_cancel(self.update_timer)

    def update(self):
        self.country_label.configure(text=self.zone)
        self.time_label.configure(text=self.get_time())
        self.date_label.configure(text=self.get_date())

        self.update_timer = self.window.after(250, self.update)

    def change_country(self):
        self.countries_label.selection_clear()
        self.zone = self.countries_label.get()
