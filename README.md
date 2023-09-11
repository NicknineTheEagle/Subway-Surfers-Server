Subway Surfers
=====

This is custom server code for old versions of Subway Surfers with now defunct servers. It is written in Python 3 and intended to be used on HTTP server with mod-wsgi installed.

You need to redirect hoodrunner.kiloo.com domain to your server and alias scripts on the server as follows:
   * /hr_dailyquests.php -> hr_dailyquests.py
   * /onlinesettings.php -> onlinesettings.py

The following server end points are known to exist in old versions of the game:

   * /hr_dailyquests.php - provides words for Daily Challenge/Word Hunt. Request/response format remained completely unchanged at least up until 2020.
   * /onlinesettings.php - initially just informed the game of new versions. In later versions provides unlock/expiry times for characters and boards and informs the game of active discounts.
   * /register.php - registers the user in the leaderboards system.
   * /report.php - uploads high score to the leaderboards.
   * /friends.php - synchronizes friends list between Facebook and the game.
   * /scores.php - fetches high scores of the user's friends.
   * /poke.php - pokes the specified friend?..
   * /brag.php - brags about the new high score to the user's friends.

Most of these got replaced with "2" versions over time, i.e. hr_dailyquests2.php, onlinesettings2.php, register2.php, probably due to format changes.
