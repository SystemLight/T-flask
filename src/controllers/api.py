from flask import Blueprint
from flask_restful import Api, Resource

api_controller = Blueprint("api", __name__)
api = Api(api_controller)


@api.resource("/trial")
class TrialApp(Resource):

    def get(self):
        return {"msg": "ok api"}
