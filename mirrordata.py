import datetime
import json
import time

import requests
import wifi
from flask import Flask, redirect, request


class Weather:
    city = None

    def __init__(self, language, temp_unit, location_request_token, wifi_addresses, weather_request_token):
        self.language = language
        self.temp_unit = temp_unit

        self.location_request_token = location_request_token
        self.wifi_addresses = wifi_addresses

        self.weather_request_token = weather_request_token

        self.country, self.latitude, self.longitude = self.request_location()

    def request_location(self):
        wifi_addresses = [cell.address for cell in wifi.Cell.all("wlan0")] if not self.wifi_addresses else self.wifi_addresses

        data = {
            "token": self.location_request_token,
            "wifi": [{"bssid": address} for address in wifi_addresses],
            "accept-language": self.language,
            "address": 2
        }

        try:
            response = requests.post("https://eu1.unwiredlabs.com/v2/process.php", data=json.dumps(data)).json()
            address_info = response.get("address_detail")

            return address_info.get("country"), response.get("lat"), response.get("lon")
        except requests.exceptions.RequestException:
            return None

    def request_weather(self):
        try:
            response = requests.get("https://api.openweathermap.org/data/2.5/find?lat={}&lon={}&cnt=1&units={}&lang={}&appid={}"
                                    .format(self.latitude, self.longitude, self.temp_unit, self.language, self.weather_request_token)).json()
            result_weather = response.get("list")[0]

            self.city = result_weather.get("name")

            main_section = result_weather.get("main")
            weather_section = result_weather.get("weather")[0]

            icon_url = "http://openweathermap.org/img/wn/{}@2x.png".format(weather_section.get("icon"))

            return round(main_section.get("temp")), weather_section.get("description"), icon_url
        except requests.exceptions.RequestException:
            return None


class Spotify:
    flask_port = 8888

    @staticmethod
    def current_millis():
        return int(round(time.time() * 1000))

    def __init__(self, app_id, app_secret, refresh_token):
        self.app_id = app_id
        self.app_secret = app_secret
        self.refresh_token = refresh_token

        flask_app = Flask(__name__)

        @flask_app.route("/", methods=["GET"])
        def spotify_login():
            return redirect("https://accounts.spotify.com/authorize"
                            "?client_id={}"
                            "&response_type=code"
                            "&redirect_uri=http%3A%2F%2F127.0.0.1:{}%2Fcallback"
                            "&scope=user-read-currently-playing%20user-read-playback-state"
                            .format(self.app_id, self.flask_port))

        @flask_app.route("/callback", methods=["GET"])
        def login_callback():
            if "code" in request.args:
                code = request.args.get("code")
                self.auth_token, self.refresh_token = self.request_token(code)
                return f"Auth-Token: {self.auth_token} <br/> Refresh-Token: {self.refresh_token}"
            return "Failed to auth!"

        if not refresh_token:
            flask_app.run(port=self.flask_port)
        else:
            self.auth_token, self.expire_millis = self.request_fresh_token(refresh_token)

    def request_token(self, auth_code):
        response = requests.post("https://accounts.spotify.com/api/token", data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": "http://127.0.0.1:{}/callback".format(self.flask_port),
            "client_id": self.app_id,
            "client_secret": self.app_secret
        })
        return response.json().get("access_token"), response.json().get("refresh_token")

    def request_fresh_token(self, refresh_token):
        response = requests.post("https://accounts.spotify.com/api/token", data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.app_id,
            "client_secret": self.app_secret
        })
        return response.json().get("access_token"), (response.json().get("expires_in") * 1000) + self.current_millis()

    def auth_headers(self):
        if self.current_millis() >= self.expire_millis:
            self.auth_token, self.expire_millis = self.request_fresh_token(self.refresh_token)

        return {
            "Authorization": f"Bearer {self.auth_token}"
        }

    def request_current_device(self):
        response = requests.get("https://api.spotify.com/v1/me/player/devices", headers=self.auth_headers())

        if response.status_code == 200:
            devices = response.json().get("devices")

            return next(filter(lambda device: device.get("is_active"), devices), {}).get("name")

        return None

    def request_current_song(self):
        response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=self.auth_headers())

        is_playing = True if response.content else False

        if response.status_code == 200 and is_playing and response.json().get("item"):
            item = response.json().get("item")

            song_name = item.get("name")
            artists = [artist.get("name") for artist in item.get("artists")]
            cover_image_url = item.get("album").get("images")[0].get("url")

            return song_name, ", ".join(artists), cover_image_url
        return "", "", ""


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
