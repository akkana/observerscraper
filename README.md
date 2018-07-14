# observerscraper

Scrape the web page from an Ambient Weather Observer, modify it
and serve it as a new website.

Ambient Weather stations have good sensors and are good choices
for people concerned with accuracy. Unfortunately, they make it rather
difficult to get your own data.

They have an API that provides JSON data, but it reads from their
website, and then it's still uncorrected for factors like elevation.

Or you can install their "WiFi Observer", which reads data from the
weather station and makes it available on your local LAN as a web page.
But the Observer has no option for JSON or another easily machine
readable format.
So the code here scrapes the Observer's web page, parses the
data and lets you make local changes before making it available
as a new web page on your local LAN.

Uses Python 3, BeautifulSoup4 to scrape the web page and
Python bottle to serve the generated web page.

## Configuration

You can put configuration files either in ~/.config/observerscraper
(for testing) or /etc/observerscraper.

Inside one of those directories, put the URL for the observer in
a file named *config*, like this:
```
url = http://192.168.1.nn
```

You may optionally also specify an order for the keys read from the
observer, such as rainofhourly, in a file named "order".
See observerscraper.py for the list of keys I see on my observer,
but if yours are different (try View Source on the observer's web page),
you can add more, though there is currently no way to add "pretty names"
corresponding with the keys.

Blank lines inside the order file will translate to blank space
in the generated web page. Comments in the order file will be ignored.

## Running

Once you have the URL specified in a config file,
run the server/scraper with:
```
./wxserver.py
```

To view the result in a browser:
[http://localhost:8080/](http://localhost:8080/)
or, from another machine,
*http://address-of-your-machine:8080/*
