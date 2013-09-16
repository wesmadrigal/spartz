#!/usr/bin/env python
import datetime

class GeoData(object):
    def __init__(self, conn, _id, fbid, name, lat, lon, continent, country, province, city, updated):
        self._conn = conn
        self._id = _id
        self._fbid = fbid
        self._name = name
        self._lat = lat
        self._lon = lon
        self._continent = continent
        self._country = country
        self._province = province
        self._city = city
        self._updated = updated
    
    def save(self):
        c = self._conn.cursor()
        c.execute("insert into geodata values(?,?,?,?,?,?,?,?,?,?)", (self._id, self._fbid, self._name, self._lat, self._lon, self._continent, self._country, self._province, self._city, self._updated))
        self._conn.commit()
        print "Values inserted"
    
