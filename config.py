# Time

WEEKDAYS = {
    0: "Montag",
    1: "Dienstag",
    2: "Mittwoch",
    3: "Donnerstag",
    4: "Freitag",
    5: "Samstag",
    6: "Sonntag"
}

# Weather

LOCATION_REQUEST_TOKEN = ""
LOCATION_REQUEST_URL = "https://eu1.unwiredlabs.com/v2/process.php"
WIFI_ADDRESSES = []  # This can be left empty if executed on a unix-based system. If not, you have to enter the mac addresses of nearby wifi networks

WEATHER_REQUEST_TOKEN = ""
WEATHER_REQUEST_URL = "https://api.openweathermap.org/data/2.5/find?lat={}&lon={}&cnt=1&units=metric&lang=de&appid=" + WEATHER_REQUEST_TOKEN

# Spotify

SPOTIFY_APP_ID = ""
SPOTIFY_APP_SECRET = ""
SPOTIFY_REFRESH_TOKEN = ""

# Cover lessons

COVER_LESSONS_HEADER = "Vertretungsplan für heute"
COVER_LESSONS_HEADER_EMPTY = "Heute fällt leider nichts aus :("

LESSON_COVERED = "{}. Stunde {} '{}' vertreten von {}"
LESSON_FREE = "{}. Stunde {} '{}'{}"

COVER_LESSONS_UUID = ""
COVER_LESSONS_URL = f"URL/{COVER_LESSONS_UUID}.json"
