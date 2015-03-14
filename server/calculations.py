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

    def check_intersect(self):
        bomliste = self.get_raw_coords()
        a = bomliste[0]
        b = bomliste[1]
        c = bomliste[2]
        d = bomliste[3]

        print great_circle(a, b).miles
        print great_circle(c, d).miles
        return great_circle(a, b).meters


print BomCalc().get_raw_coords()
print BomCalc().check_intersect()
