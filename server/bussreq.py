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
        divdata = data['data-tm-map-options']
        return divdata.encode('utf-8')

# hjelpemetode under utvikling
    def requestAndSoup(self, lang, fra, to, time, date, direction):
        requestet = self.getRequest(lang, fra, to, time, date, direction)
        dataen = self.soupifyRequest(requestet.content)
        jsondata = json.loads(dataen)
        return jsondata


br = BussRequest().requestAndSoup('no', 'havreveien%20(Kristiansand)',
                                  'uia%20v/spicheren%20(kristiansand)',
                                  '15:21', '16.03.2015', '1')

print br["TripData"]["i"][0]["n"]
print br["TripData"]["i"][1]["n"].encode("utf-8")
print br["TripData"]["i"][2]["n"].encode("utf-8")
print br["TripData"]["i"][3]["n"].encode("utf-8")
