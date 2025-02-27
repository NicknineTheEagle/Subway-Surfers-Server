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

    params+="[chartboost_delay_seconds]%d" % 30

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
    #params+="[videoads_defaultreward]%d" % 100

    # Added in 1.5.0
    # Facebook integration and leaderboards
    params+="[social_report_min_seconds]%d" % 1200
    params+="[social_report_games_count]%d" % 5
    params+="[social_consolidate_min_seconds]%d" % 3600
    params+="[social_register_min_seconds]%d" % 3600
    params+="[social_friendscores_min_seconds]%d" % 120

    # Added in 1.6.0
    # Start and expiry times for limited time characters and boards.
    # Set expire time to "disabled" to remove the item from the store
    # regardless of the current date.
    # Zombie Jake (Halloween Special)
    #params+="[character_starttime_zombiejake]%s" % "23-10-2012 00:00:00"
    #params+="[character_expiretime_zombiejake]%s" % "05-11-2012 00:00:00"
    # Elf Tricky (Holiday Special)
    #params+="[character_starttime_elftricky]%s" % "19-11-2012 00:00:00"
    #params+="[character_expiretime_elftricky]%s" % "01-01-2013 00:00:00"
    # Tony (New York Special)
    #params+="[character_starttime_tony]%s" % "02-12-2012 00:00:00"
    #params+="[character_expiretime_tony]%s" % "02-01-2013 00:00:00"
    # Liberty board (New York Special)
    #params+="[hoverboard_starttime_liberty]%s" % "02-12-2012 00:00:00"
    #params+="[hoverboard_expiretime_liberty]%s" % "02-01-2013 00:00:00"

    # Added in 1.8.0
    params+="[enable_local_notifications]%s" % "True"

    # Added in 1.9.0
    params+="[offerwall_number_of_earners]%d" % 8 # Set to "disabled" to disable the offer wall
    params+="[offerwall_session_timeout]%d" % 43200
    params+="[offerwall_offers_timeout]%d" % 30
    params+="[offerwall_balance_timeout]%d" % 60
    params+="[offerwal_min_reward_allowed]%d" % 10
    params+="[offerwall_max_reward_allowed]%d" % 20000
    params+="[offerwall_filter_min_max_reward]%s" % "True"
    params+="[offerwall_filter_free]%s" % "True"
    params+="[offerwall_filter_cost_per_install]%s" % "True"
    params+="[offerwall_offer_order]%d" % 1 # 0 - descending, 1 - ascending

    # Soft launch for revival mechanic
    #params+="[save_me_locales]%s" % "da_DK;nl_NL;ru_RU" # all - everywhere, none - nowhere
    params+="[save_me_locales]%s" % "all"

    sha1=hashlib.sha1()
    sha1.update(params.encode())
    sha1.update(b"resxrctrv7tgv7gb8h9h9u0909kllfmolkjnhghgjjkhjghg")

    responseBody=sha1.hexdigest()+"\r\n"+params

    status="200 OK"
    responseHeaders=[("Content-Type", "text/plain")]
    start_response(status,responseHeaders)
    return [responseBody.encode()]
