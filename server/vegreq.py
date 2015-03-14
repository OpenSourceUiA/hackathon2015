# -*- coding: utf-8 -*-

import requests
import json


class VegRequest(object):
    url = "http://vegvesen.no/nvdb/api"

    def getObjekt(self, objekt):
        r = requests.get(self.url + "/vegobjekter/objekt/"+objekt)
        jsonr = json.loads(r.content)
        return jsonr

    def getObjektList(self, objekt):
        r = requests.get(self.url + "/vegobjekter/"+objekt)
        jsonr = json.loads(r.content)
        return jsonr

    def sok(self, kriterier):

        leftcurlbrack = "%7B"
        rightcurlbrack = "%7D"
        colon = "%3A"
        space = "%20"
        leftbrack = "%5B"
        rightbrack = "%5D"
        dubquot = "%22"
        comma = "%2C"

        searchstring2 = leftcurlbrack\
            + "lokasjon" + colon + leftcurlbrack\
            + space + "kommune" + colon + space + leftbrack + dubquot\
            + kriterier + dubquot\
            + rightbrack + space\
            + rightcurlbrack + comma+space\
            + "objektTyper" + colon + space + leftbrack + leftcurlbrack\
            + "id" + colon + space + "45" + comma + space\
            + "antall" + colon + "10" + rightcurlbrack\
            + rightbrack + rightcurlbrack

        r = requests.get(self.url + "/sok?kriterie=" + searchstring2
                + "&assosiasjoner=false" + "&egenskaper=false")
        rjson = json.loads(r.content)
        return rjson


# print VegRequest().getObjekt("487458622")
objlist = VegRequest().getObjektList("45")
# print objlist['vegObjekter'][9]["egenskaper"]
krsbom = VegRequest().sok("1001")
print krsbom['resultater'][0]['vegObjekter'][0]['self']['uri']
