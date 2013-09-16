#!/usr/bin/env python
import json
import urllib2
import sqlite3
import sys
import csv
import re
import os
import time
from geodata import continents, countries
from models import GeoData

"""
    Takes a csv file path as command line argument, parses the data and stores it in the database
"""

api = 'http://nominatim.openstreetmap.org/reverse?format=json&lat={0}&lon={1}&zoom=18&addressdetails=1'
                 
                

def store_data_db(path):
    global api
    data = format_data(path) 
    # for the latitude and longitude coords
    sequence = re.compile(r'[0-9]+[.][0-9]+')

    conn = sqlite3.connect('schema.db')
    conn.text_factory = str 
    for _set in data[1:]: 
        # need id, fbid, name, lat, lon, continent, country, province, city
        d = _set[0].split(',')
        # data is in the form '"data"' so we must handle the erroneous string denotation
        _id = d[0].strip('"')
        fbid = d[1].strip('"')
        if len(d) == 5:
            name = d[2].strip('"')
        elif len(d) == 6:
            one = d[2].strip('"')
            two = d[3].strip('"')
            name = ','.join( [one, two] )
            name = name.strip('"')

        coords = [ i for i in d if len(re.findall(sequence, i)) > 0 ]
        if len(coords) > 1:
            lat, lon = coords[0].strip('"'), coords[1].strip('"')
            formatted = api.format(lat, lon)
            res = urllib2.urlopen(formatted).read()
            res = json.loads(res)
            country_code = res['address']['country_code'].upper()

            try:
                country = countries[country_code]['name']
            except KeyError:
                if 'country' in res['address'].keys():
                    country = res['address']['country']
                else:
                    country = 'NULL'

            if 'continent' in res['address'].keys():
                continent = res['address']['continent']
            else:
                conts = []
                for cont in continents.keys():
                    for count in continents[cont]['countries']:
                        if country == countries[count]['name']:
                            conts.append(cont)
                if len(conts) > 0:
                    continent = continents[conts[0]]['name']
                else:
                    continent = 'NULL'

            if 'state' in res['address'].keys():
                state_province = res['address']['state']
            else:
                #print "state not an available key"
                state_province = 'NULL'
 
            if 'town' in res['address'].keys():
                city = res['address']['town']
            elif 'city' in res['address'].keys():
                #print "city instead of town"
                city = res['address']['city']
            else:
                city = 'NULL'

            # handle unicode errors
            # difference encodings from csv and api hence the inconsistent encoding/decoding methods                
            facebook_data = [ _id, fbid, name, lat, lon ]
            facebook = [ i.decode('latin-1').encode('utf-8') for i in facebook_data ]
            api_data = [ continent, country, state_province, city ]
            encoded = [ i.encode('utf-8') for i in api_data ]
            row = facebook + encoded
                   
            updated = int(time.time())
            G = GeoData(conn, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], updated)
            G.save()
 
        else:
            print "Hit an error and missed %s" % _set[0]
    print "Finished writing file"


def format_data(path):
    f = open(path, 'r')
    data = f.read().split('\n')
    f.close()
    data = [ i.split('\r') for i in data ]
    # pop the end off because it always is ''
    data.pop()
    return data


if __name__ == '__main__':
    if len(sys.argv) == 2:
        arg = sys.argv[1]
        os.system("sqlite3 schema.db < schema.sql")
        store_data_db(arg)
    else:
        print "Takes one path to a csv file as arguments"

