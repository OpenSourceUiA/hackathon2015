# -*- coding: utf-8 -*-

import vegreq

from geopy.distance import great_circle


class BomCalc(object):
    vegobj = vegreq.VegRequest()

    def get_raw_coords(self):
        bomliste = self.vegobj.listBom()
        coordliste = []
        for row in bomliste:
            coordliste.append((row[4], row[5]))
        return coordliste

    def check_intersect(self, intersectlist):
        bomliste = self.get_raw_coords()
        intersects = 0
        for bom in bomliste:
            for stop in intersectlist:
                if great_circle(bom, stop).meters < 150:
                    intersects += 1
        return intersects

    def check_parking(self, endpoint):
        mockparking = [("58.1493883", "7.9966805")]
        parking_hits = 0
        for parking in mockparking:
            if great_circle(parking, endpoint).meters < 300:
                parking_hits += 1
        return parking_hits
