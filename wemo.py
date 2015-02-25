# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 19:37:04 2015

@author: Nate Bitting

@description
this script is to enable dynamic scheduling of turning on/off our outside lights using
the weather underground API's solar schedule.  We'll be using the Wemo's Python API
called 'ouimeaux' to control the switch.
"""

import urllib2
import json
from ouimeaux.environment import Environment
import datetime as dt

def get_sunset():

    # Weather Underground API KEY
    KEY = ''

    # weather underground api call to get san jose's sunrise/sunset schedule
    url = 'http://api.wunderground.com/api/'+ KEY + '/astronomy/q/CA/San_Jose.json'

    # request the json request from the wunderground api
    request = urllib2.Request(url)
    data = urllib2.urlopen(request)
    astro = data.read()
    astro_json = json.loads(astro)

    # assign the sunset hour and minute
    sunset_hour = astro_json['sun_phase']['sunset']['hour']
    sunset_min = astro_json['sun_phase']['sunset']['minute']
    sunset_time = [int(sunset_hour), int(sunset_min)]

    return str(sunset_time[0]) + ":" + str(sunset[1])

if __name__ == '__main__':

    print "Starting Wemo..."
    env = Environment(with_cache=False)
    env.start()
    env.discover(20) # find the switches on the network
    print env.list_switches()
    living = env.get_switch('Living Room')
    outside = env.get_switch('Outside Lights')
    sunset = "17:54" # set initial sunset time manually
    tracker = 0

    while True:
        # get the current time
        hour = int(dt.datetime.now().hour)
        minute = int(dt.datetime.now().minute)
        second = int(dt.datetime.now().second)
        time_now = str(hour) + ":" + str(minute)

        # retreive the current day's sunset time
        if hour == 12 and minute == 12 & second == 12:

            if tracker == 0:
                sunset = get_sunset()
                print "Today's Sunset will be at " + str(sunset[0]) + ":" + str(sunset[1])
                tracker = 1 # set tracker to 1 so it doesn't pull from the API more than once

        # turn the lights on at sunset
        elif time_now == sunset:

            if living.get_state() == 0:
                living.on()
                print 'Living Room Light On'

            if outside.get_state() == 0:
                outside.on()
                print 'Outside Lights On'

        # turn the lights off at midnight
        elif hour == 00:

            if living.get_state() == 1:
                living.off()
                print 'Living Room Light Off'

            if outside.get_state() == 1:
                outside.off()
                print 'Outside Lights Off'

            # reset tracker back to 0
            tracker = 0