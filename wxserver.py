#!/usr/bin/env python3

# Scrape the web page from an Ambient Weather Observer.
# Re-serve the info as another web page, with corrected values
# and correct HTML (unlike the Ambient).

from bottle import route, run, template

import observerscraper

import os

# Config values that can be changed in the config file:
config = {
    'url' : None,
}

order = observerscraper.nameorder

def read_config_file(configfile):
    try:
        fp = open(configfile)
    except:
        return

    print("Reading config from", configfile)
    for line in fp:
        line = line.strip()
        if line.startswith('#'):
            continue
        parts = [ p.strip() for p in line.split('=') ]
        if not parts or len(parts) != 2:
            continue

        key = parts[0].lower()
        val = parts[1]

        config[key] = val
        print("Set config %s to %s" % (key, val))

    fp.close()

def read_orderfile(orderfile):
    '''Read the preferred order of keys, such as rainofhourly.
       See observerscraper.py for keys we know about
       (but if your observer uses different keys, you can add them).
       Comment lines are ignored; empty lines will be
       translated into blank space in the final web page.
    '''
    global order
    try:
        fp = open(orderfile)
    except:
        return

    print("Reading order from", orderfile)

    order = []
    for line in fp:
        line = line.strip()
        if line.startswith('#'):
            continue
        order.append(line)

    fp.close()

def read_configs():
    dirs = [ os.path.expanduser("~/.config/observerscraper"),
             "/etc/observerscraper" ]
    for d in dirs:
        read_config_file(os.path.join(d, "config"))
        read_orderfile(os.path.join(d, "order"))

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

    vals = observerscraper.scrape_page(config['url'])

    data_html = '<table>\n'

    # First, list the keys we care about, in the right order:
    for key in order:
        if not key:
            data_html += "<tr><td colspan=2>&nbsp;"
            continue
        if key in vals:
            data_html += html_line(key, vals[key])

    # Now see if there were any values we don't care about:
    for key in vals:
        if key in order:
            # We've already shown this key.
            continue
        data_html += html_line(key, vals[key])

    data_html += "</table>"
    return template('simple.tpl', title="Current Weather", content=data_html)

read_configs()

# run(host='localhost', port=8080)
# run(host='192.168.1.4', port=8080)
run(host='0.0.0.0', port=8080)

