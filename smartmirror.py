import tkinter
import datetime


class TimeFrame(tkinter.Frame):
    time_label = None
    date_label = None

    def __init__(self, master, weekday_names):
        super().__init__(master, background="black")
        self.weekday_names = weekday_names

        self.create_widgets()
        self.update()

    def create_widgets(self):
        self.time_label = tkinter.Label(self, font=("Helvetica", 100), background="black", foreground="white")
        self.time_label.pack(side="top", anchor="e", padx=5)

        self.date_label = tkinter.Label(self, font=("Helvetica", 25), background="black", foreground="white")
        self.date_label.pack(side="top", anchor="e", padx=12.5)

    def update(self):
        now = datetime.datetime.now()

        self.time_label["text"] = now.strftime("%H:%M")
        self.date_label["text"] = f"{self.weekday_names.get(now.weekday())}, {now.strftime('%d.%m')}"

        self.time_label.after(200, self.update)


class WeatherFrame(tkinter.Frame):
    temperature_label = None
    weather_status_label = None
    location_label = None

    def __init__(self, master):
        super().__init__(master, background="black")

        self.create_widgets()
        self.update()

    def create_widgets(self):
        self.temperature_label = tkinter.Label(self, font=("Helvetica", 80), background="black", foreground="white")
        self.temperature_label.pack(side="top", anchor="w", padx=5)

        self.weather_status_label = tkinter.Label(self, font=("Helvetica", 30), background="black", foreground="white")
        self.weather_status_label.pack(side="top", anchor="w", padx=12.5)

        self.location_label = tkinter.Label(self, font=("Helvetica", 15), background="black", foreground="white")
        self.location_label.pack(side="top", anchor="w", padx=12.5)

    def update(self):
        # TODO: Get real weather
        self.temperature_label["text"] = "7°"
        self.weather_status_label["text"] = "leicht bewölkt"
        self.location_label["text"] = "Köln, Deutschland"


root = tkinter.Tk()
root.attributes("-fullscreen", True)
root.configure(background="black")

top_frame = tkinter.Frame(root, background="black")
top_frame.pack(side="top", fill="both", expand="yes")

TimeFrame(top_frame, {
    0: "Montag",
    1: "Dienstag",
    2: "Mittwoch",
    3: "Donnerstag",
    4: "Freitag",
    5: "Samstag",
    6: "Sonntag"
}).pack(side="right", anchor="n")
WeatherFrame(top_frame).pack(side="left", anchor="n")

root.mainloop()
