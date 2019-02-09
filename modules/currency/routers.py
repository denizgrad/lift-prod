from json import dumps

from flask import Response
from flask_restful import Resource

from modules.currency.controller import Controller
from modules.user.auth.routers import token_required
from resources import app


@app.api.resource('/api/v1/currency/rates/update')
class route_UpdateRates(Resource):
    def __init__(self):
        self.jobs = Controller()

    @token_required
    def get(self):
        try:
            self.jobs.update_rates()
        except Exception as e:
            print("*** failed route_UpdateRates e:{}\ne.traceback: {}\ne.args: {}".format(e, e.with_traceback, e.args))
            return Response(dumps({'status': "failed"}), status=500, mimetype='application/json')
        return Response(dumps({'status': "success"}), status=200, mimetype='application/json')


app.logger.debug("*** RouteCurrency api")


