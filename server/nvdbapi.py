import requests
import json
# import pdb

def sok( objektTyper, lokasjon='', geometriType = '' ):
    """Soeker NVDB api'et for alle objekter
    Se https://www.vegvesen.no/nvdb/api/sok for definisjon av
    objektliste (obligatorisk), lokasjon (valgfritt) og
    geometriType (valgfritt)
    Returnerer JSON objekt evt FALSE hvis noe gaar galt.
    """

    url = 'https://www.vegvesen.no/nvdb/api/sok'

    #
    if lokasjon: # Valgfritt
        parametre = { 'kriterie' : json.dumps(
                                                {
                                                    'lokasjon' : lokasjon,
                                                    'objektTyper' : objektTyper
                                                }
                                            )
                        }
    else:
        parametre = {
            'kriterie' : json.dumps(
                                        { 'objektTyper' : objektTyper }
                                    )
        }

    # For annet enn UTM33 skal fretrukket geometritype (koordinatsystem)
    # angis eksplisitt
    if geometriType:
        parametre['geometri'] = geometriType

    headers = { 'Accept' : 'application/vnd.vegvesen.nvdb-v1+json' }

    # Fornuftig feilhaandtering maa tilpasses rammeverket som bruker funksjonen
    try:
        r = requests.get( url, params = parametre, headers = headers,
                    verify = False )
    except Exception, e:
       print str(e)
       return False

    # Har vi faatt det vi vil ha?
    if (r.status_code != 200) or (headers['Accept'] not in r.headers['content-type']):
        raise ValueError(  "Expecting JSON data from the NVDB api!" +
                        "\n\tHttp status: " + str( r.status_code) +
                        "\n\tcontent-type: " + r.headers['content-type'] )
    else:
        return r.json()

if __name__=="__main__":
    data = sok( [{'id': 45, 'antall': 1}] )
    if data:
        json.dumps(data, indent=4, separators=(',', ': '))
    else:
        print "fant ingen data...?"


