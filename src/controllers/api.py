from flask import Blueprint
from flask_restful import Api, Resource

api_controller = Blueprint("api", __name__)
api = Api(api_controller)


class TrialApp(Resource):

    def get(self):
        return {"msg": "ok api"}


api.add_resource(TrialApp, "/trial")
