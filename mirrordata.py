import requests
import datetime
import wifi
import json


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
        from_today = filter(lambda cover_lesson: self.parse_time(cover_lesson.get("date")) == datetime.date.today(), cover_lessons)
        return sorted(from_today, key=lambda cover_lesson: cover_lesson.get("period"))


class Weather:

    def __init__(self, location_request_url, location_request_token, wifi_addresses, weather_request_url):
        self.location_request_url = location_request_url
        self.location_request_token = location_request_token
        self.wifi_addresses = wifi_addresses

        self.weather_request_url = weather_request_url

        self.city, self.country, self.latitude, self.longitude = self.request_location()

    def request_location(self):
        wifi_addresses = wifi.Cell.all("wlan0").keys() if not self.wifi_addresses else self.wifi_addresses

        data = {
            "token": self.location_request_token,
            "wifi": list(map(lambda address: {"bssid": address}, wifi_addresses)),
            "accept-language": "de",
            "address": 2
        }

        try:
            response = requests.post(self.location_request_url, data=json.dumps(data)).json()
            address_info = response.get("address_detail")

            return address_info.get("city"), address_info.get("country"), response.get("lat"), response.get("lon")
        except requests.exceptions.RequestException:
            return None

    def request_weather(self):
        try:
            response = requests.get(self.weather_request_url.format(self.latitude, self.longitude)).json()
            result_weather = response.get("list")[0]

            main_section = result_weather.get("main")
            weather_condition = result_weather.get("weather")[0].get("description")

            return round(main_section.get("temp")), weather_condition
        except requests.exceptions.RequestException:
            return None
