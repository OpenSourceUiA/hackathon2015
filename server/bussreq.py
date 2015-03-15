# -*- coding: utf-8 -*-
# http://rp.akt.no/scripts/TravelMagic/TravelMagicWE.dll/svar?lang=no&from=havreveien%20(kristiansand)&to=uia%20v/spicheren%20(kristiansand)&time=01:21&date=15.03.2015&direction=1
import requests
from bs4 import BeautifulSoup
import json


class BussRequest(object):
    url = "http://rp.akt.no/scripts/TravelMagic/TravelMagicWE.dll/svar?"

    def getRequest(self, lang, fra, to, time, date, direction):
        r = requests.get(self.url+'?lang='+lang+'&from='+fra+'&to='+to+'&time='
                         + time+'&date='+date+'&direction'+direction)
        return r

    def soupifyRequest(self, request):
        soup = BeautifulSoup(request)
        data = soup.find("div", {"id": "tm-result9-mapdiv"})
        if data is None:
            spans = soup.find_all("a", {"title": lambda x: x and
                                  x.startswith("Fra")})
            print "====spantext begin===="

            print "====spantext end===="
            divdata = []
            for row in spans:
                divdata.append(row.get_text())
            print divdata
        else:
            divdata = data['data-tm-map-options'].encode('utf-8')

        return divdata

    def requestAndSoup(self, lang, fra, to, time, date, direction):
        requestet = self.getRequest(lang, fra, to, time, date, direction)
        dataen = self.soupifyRequest(requestet.content)
        print type(dataen)
        if type(dataen) is list:
            dataout = dataen
        else:
            print dataen
            dataout = json.loads(dataen)
        return dataout

    def get_coords(self, lang, fra, to, time, date, direction):
        data = self.requestAndSoup(lang, fra, to, time, date, direction)
        coordlist = []
        for i in data["TripData"]["i"]:
            coordlist.append((i["y"], i["x"]))
        return coordlist


# br = BussRequest().requestAndSoup('no', 'havreveien%20(Kristiansand)',
#                                  'uia%20v/spicheren%20(kristiansand)',
#                                  '15:21', '16.03.2015', '2')


# r = requests.get("http://rp.akt.no/scripts/TravelMagic/TravelMagicWE.dll/\
#        svar?lang=no&from=havr&to=uia%20v/spicheren%20(kristiansand)&time=15:00&date=15.03.2015&direction=1")
# print r.content
