import urllib.parse
import hashlib

# Request URI: http://hoodrunner.kiloo.com/onlinesettings.php

refreshInterval=1800 # 30 minutes

ios_version="1.4.0"
ios_changelog = \
"""Placeholder changelog"""

android_version="1.0.3"
android_changelog = \
"""We've implemented an exit-button due to popular demand and optimized performance on some devices.
And addition to that we made minor bug fixes.
JOIN the world famous chase.
Help Jake escape from the grumpy Inspector!"""

def application(environ, start_response):
    queryStr=environ.get("QUERY_STRING","")
    reqParams=urllib.parse.parse_qs(queryStr,keep_blank_values=True)
    isAndroid="android" in reqParams

    params="[refreshinterval]%d" % refreshInterval
    if isAndroid:
        params+="[latestversion]%s" % android_version
        params+="[latestversion_changelist]%s" % android_changelog
    else:
        params+="[latestversion]%s" % ios_version
        params+="[latestversion_changelist]%s" % ios_changelog

    sha1=hashlib.sha1()
    sha1.update(params.encode())
    sha1.update(b"resxrctrv7tgv7gb8h9h9u0909kllfmolkjnhghgjjkhjghg")

    responseBody=sha1.hexdigest()+"\r\n"+params

    status="200 OK"
    responseHeaders=[("Content-Type", "text/plain")]
    start_response(status,responseHeaders)
    return [responseBody.encode()]
