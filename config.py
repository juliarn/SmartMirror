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
COVER_LESSONS_HEADER_EMPTY = "Heute fällt leider nichts aus :("

LESSON_COVERED = "{}. Stunde {} '{}' vertreten von {}"
LESSON_FREE = "{}. Stunde {} '{}'{}"

COVER_LESSONS_UUID = "UUID"
COVER_LESSONS_URL = f"url/{COVER_LESSONS_UUID}.json"

# Weather

LOCATION_REQUEST_URL = "http://free.ipwhois.io/json/?lang=de"

WEATHER_REQUEST_KEY = "REQUEST_KEY"
WEATHER_REQUEST_URL = "https://api.openweathermap.org/data/2.5/find?q={}&units=metric&lang=de&appid=" + WEATHER_REQUEST_KEY
