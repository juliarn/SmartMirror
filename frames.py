import tkinter
import datetime

import config


class MirrorLabel(tkinter.Label):

    def __init__(self, master, font_size):
        super().__init__(master, font=("Helvetica", font_size), background="black", foreground="white")


class TimeFrame(tkinter.Frame):
    time_label = None
    date_label = None

    def __init__(self, master, weekday_names):
        super().__init__(master, background="black")
        self.weekday_names = weekday_names

        self.create_widgets()
        self.update()

    def create_widgets(self):
        self.time_label = MirrorLabel(self, 105)
        self.time_label.pack(side="top", anchor="e", padx=5)

        self.date_label = MirrorLabel(self, 25)
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

    def __init__(self, master, weather):
        super().__init__(master, background="black")
        self.weather = weather

        self.create_widgets()
        self.update()

    def create_widgets(self):
        self.temperature_label = MirrorLabel(self, 80)
        self.temperature_label.pack(side="top", anchor="w", padx=5)

        self.weather_status_label = MirrorLabel(self, 25)
        self.weather_status_label.pack(side="top", anchor="w", padx=12.5)

        self.location_label = MirrorLabel(self, 16)
        self.location_label.pack(side="top", anchor="w", padx=12.5)

    def update(self):
        temperature, max_temperature, min_temperature, weather_condition = self.weather.request_weather()

        self.temperature_label["text"] = f"{temperature}°"
        self.weather_status_label["text"] = f"{weather_condition} ({max_temperature}°/{min_temperature}°)"
        self.location_label["text"] = f"{self.weather.city}, {self.weather.country}"

        self.temperature_label.after(1000 * 60 * 15, self.update)


class CoverLessonFrame(tkinter.Frame):
    head_label = None
    lesson_labels = []

    def __init__(self, master, cover_lessons):
        super().__init__(master, background="black")
        self.cover_lessons = cover_lessons

        self.create_widgets()
        self.update()

    def create_widgets(self):
        self.head_label = MirrorLabel(self, 20)
        self.head_label.pack(side="top", anchor="w", padx=12.5, pady=4)

    def update(self):
        self.cover_lessons.update()

        head_label_text = config.COVER_LESSONS_HEADER if self.cover_lessons.cover_lessons else config.COVER_LESSONS_HEADER_EMPTY
        self.head_label["text"] = head_label_text

        for lesson_label in self.lesson_labels:
            lesson_label.destroy()

        for cover_lesson in self.cover_lessons.cover_lessons:
            lesson_label = MirrorLabel(self, 15)
            lesson_label.pack(side="top", anchor="w", padx=30)

            self.lesson_labels.append(lesson_label)

            teacher = cover_lesson.get("teacher") if cover_lesson.get("teacher") else ""
            label_text = config.LESSON_COVERED if teacher else config.LESSON_FREE

            lesson_label["text"] = label_text.format(cover_lesson.get("period"), cover_lesson.get("subject"), cover_lesson.get("comment"), teacher)

        self.head_label.after(1000 * 60 * 60, self.update)
