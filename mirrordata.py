import datetime
import json
import time

import requests
import wifi
from flask import Flask, redirect, request


class Weather:

    def __init__(self, location_request_url, location_request_token, wifi_addresses, weather_request_url):
        self.location_request_url = location_request_url
        self.location_request_token = location_request_token
        self.wifi_addresses = wifi_addresses

        self.weather_request_url = weather_request_url

        self.city, self.country, self.latitude, self.longitude = self.request_location()

    def request_location(self):
        wifi_addresses = list(map(lambda cell: cell.address, wifi.Cell.all("wlan0"))) if not self.wifi_addresses else self.wifi_addresses

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
                            "&scope=user-read-currently-playing"
                            .format(self.app_id, self.flask_port))

        @flask_app.route("/callback")
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

    def request_current_song(self):
        if self.current_millis() >= self.expire_millis:
            self.auth_token, self.expire_millis = self.request_fresh_token(self.refresh_token)

        headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }
        response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)

        is_playing = True if response.content else False

        if is_playing:
            item = response.json().get("item")

            if not item:
                return "", ""

            song_name = item.get("name")
            artists = [artist.get("name") for artist in item.get("artists")]

            return song_name, ", ".join(artists)
        return "", ""


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
