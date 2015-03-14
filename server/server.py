from flask import Flask
from flask.ext.restful import Api, Resource, reqparse
from bussreq import BussRequest
import calculations

app = Flask(__name__)
api = Api(app)


class BussAPI(Resource):
    br = BussRequest()

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('lang', type=str, required=False, help="No \
                language provided")
        self.reqparse.add_argument('fra', type=str, required=True, help="No \
                from position  provided")
        self.reqparse.add_argument('to', type=str, required=True, help="No \
                from position provided")
        self.reqparse.add_argument('time', type=str, required=True, help="No \
                time provided")
        self.reqparse.add_argument('date', type=str, required=True, help="No \
                date provided")
        self.reqparse.add_argument('direction', type=str, required=True, help="No \
                direction provided")
        super(BussAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        print args
        lang = args['lang']
        fra = args['fra']
        to = args['to']
        time = args['time'].replace("-", ":")
        print time
        date = args['date']
        print date
        direction = args['direction']
        rAS = self.br.requestAndSoup(lang, fra, to, time, date, direction)
        if type(rAS) is list:
            print rAS
        else:
            intersects = calculations.BomCalc().check_intersect(
                    self.br.get_coords(lang, fra, to, time, date, direction))
            rAS["TripData"]["Bomringer"] = intersects
        return rAS, 201


class ParkingAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('x', type=str, required=True, help="No X \
                coordinate given", location="json")
        self.reqparse.add_argument('y', type=str, required=True, help="no Y \
                coordinate given", location="json")
        super(ParkingAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        parkings = calculations.BomCalc().check_parking((args["y"], args["x"]))
        return parkings


class AlertsAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('x', type=str, required=True, help="No X \
                coordinate given", location="json")
        self.reqparse.add_argument('y', type=str, required=True, help="No Y \
                coordinate given", location="json")
        self.reqparse.add_argument('veg', type=str, location="json")
        self.reqparse.add_argument('body', type=str, required=True, help="No \
                body given", location="json")


api.add_resource(ParkingAPI, '/parking', endpoint='parking')
api.add_resource(BussAPI, '/buss', endpoint='buss')
api.add_resource(AlertsAPI, '/alerts', endpoint='alerts')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
