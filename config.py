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

# Cover lessons

COVER_LESSONS_HEADER = "Vertretungsplan für heute"
COVER_LESSONS_HEADER_EMPTY = "Keine Vertretungen gefunden"

LESSON_COVERED = "{}. Stunde {} '{}' vertreten von {}"
LESSON_FREE = "{}. Stunde {} '{}'{}"

COVER_LESSONS_UUID = "uuid"
COVER_LESSONS_URL = f"url/{COVER_LESSONS_UUID}.json"

# Weather

LOCATION_REQUEST_URL = "https://ipapi.co/json"

WEATHER_REQUEST_KEY = "API_KEY"
WEATHER_REQUEST_URL = "https://api.openweathermap.org/data/2.5/find?q={}&units=metric&appid=" + WEATHER_REQUEST_KEY
