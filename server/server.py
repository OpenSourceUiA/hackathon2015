from flask import Flask
from flask.ext.restful import Api, Resource, reqparse
from bussreq import BussRequest

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

        return self.br.requestAndSoup(lang, fra, to, time, date,
                                      direction), 201


api.add_resource(BussAPI, '/buss', endpoint='buss')


if __name__ == '__main__':
    app.run(debug=True)
