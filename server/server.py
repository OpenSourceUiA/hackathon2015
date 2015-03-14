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
        self.reqparse.add_argument('lang', type=str, required=True, help="No \
                language provided", location='json')
        self.reqparse.add_argument('fra', type=str, required=True, help="No \
                from position  provided", location='json')
        self.reqparse.add_argument('to', type=str, required=True, help="No \
                from position provided", location='json')
        self.reqparse.add_argument('time', type=str, required=True, help="No \
                time provided", location='json')
        self.reqparse.add_argument('date', type=str, required=True, help="No \
                date provided", location='json')
        self.reqparse.add_argument('direction', type=str, required=True, help="No \
                direction provided", location='json')
        super(BussAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        lang = args['lang']
        fra = args['fra']
        to = args['to']
        time = args['time']
        date = args['date']
        direction = args['direction']
        rAS = self.br.requestAndSoup(lang, fra, to, time, date, direction)
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


api.add_resource(ParkingAPI, '/parking', endpoint='parking')
api.add_resource(BussAPI, '/buss', endpoint='buss')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
