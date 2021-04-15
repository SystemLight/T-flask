from flask import Blueprint
from flask_restful import Api, Resource

bp = Blueprint("default", __name__)
api = Api(bp, prefix="/api")
