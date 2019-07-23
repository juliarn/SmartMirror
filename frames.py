import datetime
import tkinter

from PIL import ImageTk, Image

import config


class MirrorLabel(tkinter.Label):

    def __init__(self, master, font_size, font_color="white"):
        super().__init__(master, font=("Helvetica", font_size), background="black", foreground=font_color)


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
    weather_status_label = None
    location_label = None

    def __init__(self, master, weather):
        super().__init__(master, background="black")
        self.weather = weather

        self.create_widgets()
        self.update()

    def create_widgets(self):
        self.temperature_label = MirrorLabel(self, 70)
        self.temperature_label.pack(side="top", anchor="w", padx=config.SIDE_PADDING, pady=(config.SIDE_PADDING, 0))

        self.weather_status_label = MirrorLabel(self, 25)
        self.weather_status_label.pack(side="top", anchor="w", padx=config.SIDE_PADDING)

        self.location_label = MirrorLabel(self, 16)
        self.location_label.pack(side="top", anchor="w", padx=config.SIDE_PADDING)

    def update(self):
        temperature, weather_condition = self.weather.request_weather()

        self.temperature_label["text"] = f"{temperature}°"
        self.weather_status_label["text"] = weather_condition
        self.location_label["text"] = f"{self.weather.city}, {self.weather.country}"

        self.temperature_label.after(1000 * 60 * 15, self.update)


class SpotifyFrame(tkinter.Frame):
    device_label = None
    song_label = None
    artist_label = None
    cover_canvas = None

    def __init__(self, master, spotify):
        super().__init__(master, background="black")
        self.spotify = spotify

        self.create_widgets()
        self.update()

    def create_widgets(self):
        self.device_label = MirrorLabel(self, 12, font_color="grey")
        self.device_label.pack(side="top", anchor="e", padx=config.SIDE_PADDING, pady=(0, 10))

        self.cover_canvas = tkinter.Canvas(self, background="black", highlightthickness=0, width=config.SPOTIFY_COVER_SIZE, height=config.SPOTIFY_COVER_SIZE)
        self.cover_canvas.pack(side="top", anchor="e", padx=config.SIDE_PADDING, pady=(0, 10))

        self.song_label = MirrorLabel(self, 18)
        self.song_label.pack(side="top", anchor="e", padx=config.SIDE_PADDING)

        self.artist_label = MirrorLabel(self, 12)
        self.artist_label.pack(side="top", anchor="e", padx=config.SIDE_PADDING, pady=(0, config.SIDE_PADDING))

    def update(self):
        current_device = self.spotify.request_current_device()
        self.device_label["text"] = config.SPOTIFY_DEVICE_LABEL.format(current_device) if current_device else ""

        self.song_label["text"], self.artist_label["text"], cover_image_url = self.spotify.request_current_song()

        if cover_image_url:
            image = ImageTk.PhotoImage(image=Image.fromarray(self.spotify.parse_image(cover_image_url, config.SPOTIFY_COVER_SIZE)))

            self.cover_canvas.image = image
            self.cover_canvas.create_image(0, 0, image=image, anchor="nw")
        else:
            self.cover_canvas.delete("all")

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
