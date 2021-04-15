from ._base import api, Resource


@api.resource("/home")
class HomeApi(Resource):

    def get(self):
        return {"msg": "hello"}
