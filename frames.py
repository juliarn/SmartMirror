import datetime
import tkinter
from io import BytesIO

import cv2
import numpy
import requests
from PIL import ImageTk, Image

import config


class MirrorLabel(tkinter.Label):

    def __init__(self, master, font_size, font_color="white"):
        super().__init__(master, font=("Helvetica", font_size), background="black", foreground=font_color)


class MirrorImage(tkinter.Canvas):
    image = None

    @staticmethod
    def get_image_data(url):
        response = requests.get(url)
        return bytearray(response.content)

    def __init__(self, master, size):
        super().__init__(master, background="black", highlightthickness=0, width=size[0], height=size[1])
        self.size = size

    def parse_image(self, image_data, resize):
        if resize:
            image = numpy.asarray(image_data, dtype="uint8")
            image = cv2.cvtColor(cv2.imdecode(image, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
            return Image.fromarray(cv2.resize(image, self.size, interpolation=cv2.INTER_CUBIC))

        return Image.open(BytesIO(image_data))

    def set_data(self, url=None, data=None, resize=False):
        image_data = data if data else self.get_image_data(url) if url else None

        if image_data:
            self.image = ImageTk.PhotoImage(image=self.parse_image(image_data, resize))
            self.create_image(0, 0, image=self.image, anchor="nw")
        else:
            self.delete("all")


class TimeFrame(tkinter.Frame):
    time_label = None
    date_label = None

    def __init__(self, master, weekday_names):
        super().__init__(master, background="black")
        self.weekday_names = weekday_names

        self.create_widgets()
        self.update()

    def create_widgets(self):
        self.time_label = MirrorLabel(self, 95)
        self.time_label.pack(side="top", anchor="e", padx=config.SIDE_PADDING, pady=(config.SIDE_PADDING, 0))

        self.date_label = MirrorLabel(self, 25)
        self.date_label.pack(side="top", anchor="e", padx=config.SIDE_PADDING)

    def update(self):
        now = datetime.datetime.now()

        self.time_label["text"] = now.strftime("%H:%M")
        self.date_label["text"] = f"{self.weekday_names.get(now.weekday())}, {now.strftime('%d.%m')}"

        self.time_label.after(200, self.update)


class WeatherFrame(tkinter.Frame):
    temperature_label = None
    weather_status_image = None
    weather_status_label = None
    location_label = None
    weather_forecast_image = None

    def __init__(self, master, weather):
        super().__init__(master, background="black")
        self.weather = weather

        self.create_widgets()
        self.update()

    def create_widgets(self):
        temperature_frame = tkinter.Frame(self, background="black")
        temperature_frame.pack(side="top", fill="both", expand="yes", padx=config.SIDE_PADDING, pady=(config.SIDE_PADDING, 0))

        self.temperature_label = MirrorLabel(temperature_frame, 70)
        self.temperature_label.pack(side="left", anchor="n")

        self.weather_status_image = MirrorImage(temperature_frame, (100, 100))
        self.weather_status_image.pack(side="right", anchor="n")

        self.weather_status_label = MirrorLabel(self, 25)
        self.weather_status_label.pack(side="top", anchor="w", padx=config.SIDE_PADDING)

        self.location_label = MirrorLabel(self, 16)
        self.location_label.pack(side="top", anchor="w", padx=config.SIDE_PADDING)

        self.weather_forecast_image = MirrorImage(self, (400, 200))
        self.weather_forecast_image.pack(side="top", anchor="w")

    def update(self):
        temperature, self.weather_status_label["text"], icon_url = self.weather.request_weather()

        self.temperature_label["text"] = f"{temperature}°"
        self.weather_status_image.set_data(url=icon_url)

        self.location_label["text"] = f"{self.weather.city}, {self.weather.country}"

        self.weather_forecast_image.set_data(data=self.weather.create_weather_diagram())

        self.temperature_label.after(1000 * 60 * 10, self.update)


class SpotifyFrame(tkinter.Frame):
    device_label = None
    song_label = None
    artist_label = None
    cover_image = None

    def __init__(self, master, spotify):
        super().__init__(master, background="black")
        self.spotify = spotify

        self.create_widgets()
        self.update()

    def create_widgets(self):
        self.device_label = MirrorLabel(self, 12, font_color="grey")
        self.device_label.pack(side="top", anchor="e", padx=config.SIDE_PADDING, pady=(0, 10))

        self.cover_image = MirrorImage(self, (config.SPOTIFY_COVER_SIZE, config.SPOTIFY_COVER_SIZE))
        self.cover_image.pack(side="top", anchor="e", padx=config.SIDE_PADDING, pady=(0, 10))

        self.song_label = MirrorLabel(self, 18)
        self.song_label.pack(side="top", anchor="e", padx=config.SIDE_PADDING)

        self.artist_label = MirrorLabel(self, 12)
        self.artist_label.pack(side="top", anchor="e", padx=config.SIDE_PADDING, pady=(0, config.SIDE_PADDING))

    def update(self):
        current_device = self.spotify.request_current_device()
        self.device_label["text"] = config.SPOTIFY_DEVICE_LABEL.format(current_device) if current_device else ""

        self.song_label["text"], self.artist_label["text"], cover_image_url = self.spotify.request_current_song()
        self.cover_image.set_data(url=cover_image_url, resize=True)

        self.song_label.after(1000, self.update)


class CoverLessonFrame(tkinter.Frame):
    head_label = None
    lesson_labels = []

    def __init__(self, master, cover_lessons):
        super().__init__(master, background="black")
        self.cover_lessons = cover_lessons

        self.create_widgets()
        self.update()

    def create_widgets(self):
        self.head_label = MirrorLabel(self, 18)
        self.head_label.pack(side="top", anchor="w", padx=config.SIDE_PADDING, pady=(0, config.SIDE_PADDING))

    def update(self):
        self.cover_lessons.update()

        head_label_text = config.COVER_LESSONS_HEADER if self.cover_lessons.cover_lessons else config.COVER_LESSONS_HEADER_EMPTY
        self.head_label["text"] = head_label_text

        for lesson_label in self.lesson_labels:
            lesson_label.destroy()

        for cover_lesson in self.cover_lessons.cover_lessons:
            lesson_label = MirrorLabel(self, 13)
            lesson_label.pack(side="top", anchor="w", padx=config.SIDE_PADDING, pady=(0, config.SIDE_PADDING))

            self.lesson_labels.append(lesson_label)

            teacher = cover_lesson.get("teacher") if cover_lesson.get("teacher") else ""
            label_text = config.LESSON_COVERED if teacher else config.LESSON_FREE

            lesson_label["text"] = label_text.format(cover_lesson.get("period"), cover_lesson.get("subject"), cover_lesson.get("comment"), teacher)

        self.head_label.after(1000 * 60 * 60, self.update)
