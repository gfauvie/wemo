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
    url = 'http://api.wunderground.com/api/' + KEY + '/astronomy/q/CA/San_Jose.json'

    # request the json request from the wunderground api
    request = urllib2.Request(url)
    data = urllib2.urlopen(request)
    astro = data.read()
    astro_json = json.loads(astro)

    # assign the sunset hour and minute
    sunset_hour = astro_json['sun_phase']['sunset']['hour']
    sunset_min = astro_json['sun_phase']['sunset']['minute']
    sunset_time = [int(sunset_hour), int(sunset_min)]

    return sunset_time

if __name__ == '__main__':

    print "Starting Wemo..."
    # start the wemo environment
    env = Environment(with_cache=False)
    env.start()

    #search for available devices connected to the network
    env.discover(15)
    print env.list_switches()

    #assign each switch to a variable
    living = env.get_switch('Living Room')
    outside = env.get_switch('Outside Lights')
    sunset = [25, 62]

    while True:
        # get the current time
        hour = int(dt.datetime.now().hour)
        minute = int(dt.datetime.now().minute)
        second = int(dt.datetime.now().second)

        # retrieve the day's sunset time once per day
        if hour == 12 & minute == 12 & second == 12:
            sunset = get_sunset()
            print "Today's Sunset will be at " + str(sunset[0]) + ":" + str(sunset[1])

        # turn the lights on at sunset
        elif hour >= sunset[0] & minute >= sunset[1]:

            if living.get_state() == 0:
                living.on()
                print 'Living Room Light On'

            if outside.get_state() == 0:
                outside.on()
                print 'Outside Lights On'

        # turn the lights off at 11pm
        elif hour == 23:

            if living.get_state() == 1:
                living.off()
                print 'Living Room Light Off'

            if outside.get_state() == 1:
                outside.off()
                print 'Outside Lights Off'