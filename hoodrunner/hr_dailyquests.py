import urllib.parse
import hashlib
import datetime

# Request URI: http://hoodrunner.kiloo.com/hr_dailyquests.php
# You can replace words list with your own, any list length will work.
# Note that the game expects 5 letters or less.
# 6 letters or more works but looks bugged in UI.

words = [
    "GAME",
    "WHEEL",
    "CAB",
    "TOY",
    "TRIP",
    "LIGHT",
    "RAIL",
    "PIT",
    "FAN",
    "PLAZA",
    "SIGN",
    "DOOR",
    "BELL",
    "CURVE",
    "CRASH",
    "BOX",
    "TUBE",
    "SLIDE",
    "METRO",
    "ROUND",
    "TRAIN",
    "CAR",
    "RED",
    "TURBO",
    "TRACK",
    "MAP",
    "LINE",
    "BUS",
    "CITY",
    "KEY",
    "STOP",
    ]

def is_post_request(environ):
    if environ['REQUEST_METHOD'].upper() != 'POST':
        return False
    content_type = environ.get('CONTENT_TYPE', 'application/x-www-form-urlencoded')
    return (content_type.startswith('application/x-www-form-urlencoded' or
                                    content_type.startswith('multipart/form-data')))

def application(environ, start_response):
    if not is_post_request(environ):
        start_response("405 Method Not Allowed", [("Allowed", "POST")])
        return [b"POST requests only"]

    requestBody=environ["wsgi.input"].read().decode()
    reqParams=urllib.parse.parse_qs(requestBody)

    # Get the client key from POST request.
    if "key" not in reqParams:
        start_response("400 Bad Request", [])
        return [b"Bad parameters"]

    key=reqParams["key"][0]
    secretKey="aIN0UXP4NNoANVGi5w3raGAFN1n5OLQZFDhwjs6HoX"

    # Get midnight UTC of the next day and seconds until that.
    dt=datetime.datetime.now(datetime.UTC)
    nextdt=dt+datetime.timedelta(days=1)
    nextdt=datetime.datetime(nextdt.year,nextdt.month,nextdt.day,tzinfo=datetime.UTC)
    delta=nextdt-dt
    expireSec=delta.seconds

    # Get day of the year.
    dayNumber=dt.timetuple().tm_yday-1

    # Get the word from the pool based on day of the month.
    word=words[(dt.day-1) % len(words)]

    # Calculate SHA-1 hash of the resulting values.
    hashedStr=str(dayNumber)+word+str(dt.year)
    hashedStr+=key+secretKey
    hashedStr+=str(dt.month)+str(dt.day)+str(dt.hour)+str(dt.minute)+str(dt.second)+str(expireSec)
    sha1=hashlib.sha1()
    sha1.update(hashedStr.encode())

    # Build the response string.
    responseBody = "%d;%s;%d;%s;%d;%d;%d;%d;%d;%d" % (dayNumber,word,dt.year,sha1.hexdigest().lower(),
                                                      dt.month,dt.day,dt.hour,dt.minute,dt.second,
                                                      expireSec)

    status="200 OK"
    responseHeaders=[("Content-Type", "text/plain")]
    start_response(status,responseHeaders)
    return [responseBody.encode()]
