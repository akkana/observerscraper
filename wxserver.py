#!/usr/bin/env python3

# Scrape the web page from an Ambient Weather Observer.
# Re-serve the info as another web page, with corrected values
# and correct HTML (unlike the Ambient).

from bottle import route, run, template

import observerscraper

@route('/hello/<name>')
def hello(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/')
def index():
    '''Basic page showing the values the weather observer is reporting,
       scraped from its silly web page.
    '''

    def html_line(key, val):
        label = observerscraper.prettykey(key)
        if type(val) is float:
            return '<tr><td>%s <td>%.4f\n' % (label, val)
        else:
            return '<tr><td>%s <td>%s\n' % (label, val)

    vals = observerscraper.scrape_page('http://192.168.1.10/livedata.htm')

    data_html = '<table>\n'

    # First, list the keys we care about, in the right order:
    for key in observerscraper.nameorder:
        if key in vals:
            data_html += html_line(key, vals[key])

    # Now see if there were any values we don't care about:
    for key in vals:
        if key in observerscraper.nameorder:
            # We've already shown this key.
            continue
        data_html += html_line(key, vals[key])

    data_html += "</table>"
    return template('simple.tpl', title="Current Weather", content=data_html)

# run(host='localhost', port=8080)
# run(host='192.168.1.4', port=8080)
run(host='0.0.0.0', port=8080)

