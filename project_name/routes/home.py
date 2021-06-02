from ._base import bp, api, Resource


@api.resource("/home")
class HomeApi(Resource):

    def get(self):
        return {"msg": "hello"}


@bp.route("/hello")
def hello():
    return {"msg": "ok"}
