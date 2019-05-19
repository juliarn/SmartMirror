import tkinter

import config
import frames
import lessons


class SmartMirrorApplication(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.attributes("-fullscreen", True)
        self.configure(background="black")

        self.create_top_frame()
        self.create_bottom_frame()

    def create_top_frame(self):
        top_frame = tkinter.Frame(self, background="black")
        top_frame.pack(side="top", fill="both", expand="yes")

        frames.TimeFrame(top_frame, config.WEEKDAYS).pack(side="right", anchor="n")
        frames.WeatherFrame(top_frame).pack(side="left", anchor="n")

    def create_bottom_frame(self):
        bottom_frame = tkinter.Frame(self, background="black")
        bottom_frame.pack(side="bottom", fill="both", expand="yes", pady=15)

        frames.CoverLessonFrame(bottom_frame, lessons.CoverLessons(config.COVER_LESSONS_URL)).pack(side="left", anchor="s")


app = SmartMirrorApplication()
app.mainloop()
