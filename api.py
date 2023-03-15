from flask import *
from flask_restx import Api, Resource, Namespace, fields, reqparse
from math import radians, cos, sin, asin, sqrt

app = Flask(__name__)
api = Api(app, version='1.0', title="Closer Geographically Points API",
          description='An API that returns the geographically points inside a customized area.\n'+
          'It follows the Haversine formula to calculate the distance between the coordinates points.')

ns = Namespace(
    'points', description='The points that the API will evaluate.')
api.add_namespace(ns)

# TODO -> add minimum and maximum value
parser = reqparse.RequestParser()
parser.add_argument('latitude', required=True, type=float,
                    help='The latitude of the starting point.')
parser.add_argument('longitude', required=True, type=float,
                    help='The longitude of the starting point.')
parser.add_argument('range', required=True, type=float,
                    help='The range of the searching area (in kms).')


obj_lst_model = api.model('fields_lst', dict(
    latitude=fields.Float(required=True, default="40.633217", min=-90, max=90),
    longitude=fields.Float(
        required=True, default="-8.659336", min=-180, max=180),
))

points_model = api.model('list', obj_lst_model)

body = api.model('points', dict(
    points=fields.Nested(points_model, as_list=True)
))


@ns.route('/v1/inside-points')
@api.doc(responses={200: "Success"})
@api.doc(responses={404: "Points not found"})
@api.doc(responses={400: "Bad request"})
@api.doc(responses={500: "Internal Server Error"})
class CloseGeoPointsAPI(Resource):
    @api.expect(parser, body)
    def post(self):
        lst = []
        body_req = json.loads(request.data)

        for point in body_req['points']:
            lon1, lat1, lon2, lat2 = map(radians, [float(request.args.get('longitude')), float(request.args.get('latitude')),
                                                   float(point["longitude"]), float(point["latitude"])])

            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            r = 6371  # Radius of earth in kilometers.

            if (c*r <= float(request.args.get('range'))):
                lst.append(point)

        return lst


if __name__ == '__main__':
    app.run(debug=True, port=8040)
