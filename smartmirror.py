import tkinter

import config
import frames
import mirrordata


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

        weather = mirrordata.Weather(config.LOCATION_REQUEST_URL, config.WEATHER_REQUEST_URL)
        frames.WeatherFrame(top_frame, weather).pack(side="left", anchor="n")

    def create_bottom_frame(self):
        bottom_frame = tkinter.Frame(self, background="black")
        bottom_frame.pack(side="bottom", fill="both", expand="yes", pady=15)

        frames.CoverLessonFrame(bottom_frame, mirrordata.CoverLessons(config.COVER_LESSONS_URL)).pack(side="left", anchor="s")


app = SmartMirrorApplication()
app.mainloop()
