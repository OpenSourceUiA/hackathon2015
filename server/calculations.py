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
        rawbomliste = self.vegobj.listBom()
        bomliste = self.get_raw_coords()
        intersects = 0
        cost = 0
        iterator = 0
        for bom in bomliste:
            price = [rawbomliste[iterator][1], rawbomliste[iterator][2]]
            iterator += 1
            for stop in intersectlist:
                if great_circle(bom, stop).meters < 150:
                    intersects += 1
                    cost += float(price[0])
                    print cost
        finaldata = [intersects, cost]
        return finaldata

    def check_parking(self, endpoint):
        mockparking = [("58.1493883", "7.9966805")]
        parking_hits = 0
        for parking in mockparking:
            if great_circle(parking, endpoint).meters < 300:
                parking_hits += 1
        return parking_hits

    def check_fuel(self, fueleff, fuelprice, start, end):
        distance = great_circle(start, end).kilometers
        print distance
        totalprice = (float(distance)*float(fueleff))*float(fuelprice)
        print totalprice
        return totalprice
