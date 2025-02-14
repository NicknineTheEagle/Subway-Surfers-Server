import urllib.parse
import hashlib

# Request URI: http://hoodrunner.kiloo.com/onlinesettings.php

ios_version="1.0.0"
ios_changelog = \
"""Placeholder changelog"""

android_version="1.0.1"
android_changelog = \
"""We've implemented an exit-button due to popular demand and optimized performance on some devices.
And addition to that we made minor bug fixes.
JOIN the world famous chase.
Help Jake escape from the grumpy Inspector!"""

def application(environ, start_response):
    queryStr=environ.get("QUERY_STRING","")
    reqParams=urllib.parse.parse_qs(queryStr,keep_blank_values=True)
    isAndroid="android" in reqParams

    params="[refreshinterval]%d" % 3600 # 60 minutes
    if isAndroid:
        params+="[latestversion]%s" % android_version
        params+="[latestversion_changelist]%s" % android_changelog
    else:
        params+="[latestversion]%s" % ios_version
        params+="[latestversion_changelist]%s" % ios_changelog

    # Added in 1.4.0
    # Seasonal events (removed in 1.6.0)
    params+="[season]%s" % "normal" # Options: normal, halloween, xmas, easter
    params+="[end_season_datetime]%s" % "05-11-2012 00:00:00"

    # Discounts
    #params+="[in_app_tier_1]%d" % 1000 # Positive value means +N bonus coins, negative value means -%N off
    #params+="[double_coin_discount]%d" % -50
    #params+="[discount_end_time]%d" % 1739602857 # UNIX timestamp
    #params+="[discount_deal_name]%s" % "Special offer"

    # Ads
    #params+="[videoads_providerlist]%s" % "adcolony,vungleclips"
    #params+="[chartboost_delay_seconds]%d" % 30
    #params+="[videoads_defaultreward]%d" % 100

    # Added in 1.5.0
    # Facebook integration and leaderboards
    params+="[social_report_min_seconds]%d" % 1200
    params+="[social_report_games_count]%d" % 5
    params+="[social_consolidate_min_seconds]%d" % 3600
    params+="[social_register_min_seconds]%d" % 3600
    params+="[social_friendscores_min_seconds]%d" % 120

    sha1=hashlib.sha1()
    sha1.update(params.encode())
    sha1.update(b"resxrctrv7tgv7gb8h9h9u0909kllfmolkjnhghgjjkhjghg")

    responseBody=sha1.hexdigest()+"\r\n"+params

    status="200 OK"
    responseHeaders=[("Content-Type", "text/plain")]
    start_response(status,responseHeaders)
    return [responseBody.encode()]
