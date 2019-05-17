import tkinter
import datetime


class SmartMirrorApplication(tkinter.Frame):

    def __init__(self, master, weekday_names):
        super().__init__(master)
        self.master = master
        self.weekday_names = weekday_names

        self.pack()

        self.time_label = None
        self.date_label = None

        self.create_widgets()
        self.update()

    def create_widgets(self):
        self.time_label = tkinter.Label(font=("Helvetica", 100), background="black", foreground="white")
        self.time_label.pack(side="top", anchor="e")

        self.date_label = tkinter.Label(font=("Helvetica", 25), background="black", foreground="white")
        self.date_label.pack(side="top", anchor="e")

    def update(self):
        now = datetime.datetime.now()

        self.time_label["text"] = now.strftime("%H:%M")
        self.date_label["text"] = f"{self.weekday_names.get(now.weekday())}, {now.strftime('%d.%m')}"

        self.time_label.after(200, self.update)


root = tkinter.Tk()
root.attributes("-fullscreen", True)
root.configure(background="black")

app = SmartMirrorApplication(root, {
    0: "Montag",
    1: "Dienstag",
    2: "Mittwoch",
    3: "Donnerstag",
    4: "Freitag",
    5: "Samstag",
    6: "Sonntag"
})
app.mainloop()
