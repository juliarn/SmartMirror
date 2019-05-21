import requests
import datetime


class CoverLessons:
    cover_lessons = None

    @staticmethod
    def parse_time(date_string):
        return datetime.datetime.strptime(date_string, "%Y-%m-%d").date()

    def __init__(self, request_url):
        self.request_url = request_url

    def update(self):
        cover_lessons = self.request_cover_lessons()

        self.cover_lessons = self.get_from_today(cover_lessons)

    def request_cover_lessons(self):
        try:
            return requests.get(self.request_url).json().get("coverLessons")
        except requests.exceptions.RequestException:
            return []

    def get_from_today(self, cover_lessons):
        print(datetime.datetime.today())
        from_today = filter(lambda cover_lesson: self.parse_time(cover_lesson.get("date")) == datetime.date.today(), cover_lessons)
        return sorted(from_today, key=lambda cover_lesson: cover_lesson.get("period"))


class Weather:

    def __init__(self, location_request_url, weather_request_url):
        self.location_request_url = location_request_url
        self.weather_request_url = weather_request_url

        city, country_code, country = self.request_location()

        self.city = city
        self.country_code = country_code
        self.country = country

    def request_location(self):
        try:
            response = requests.get(self.location_request_url).json()
            return response.get("city"), response.get("country_code"), response.get("country")
        except requests.exceptions.RequestException:
            return None

    def request_weather(self):
        try:
            response = requests.get(self.weather_request_url.format(f"{self.city},{self.country_code}")).json()
            result_weather = response.get("list")[0]

            main_section = result_weather.get("main")
            weather_condition = result_weather.get("weather")[0].get("description")

            return round(main_section.get("temp")), round(main_section.get("temp_max")), round(main_section.get("temp_min")), weather_condition
        except requests.exceptions.RequestException:
            return None
