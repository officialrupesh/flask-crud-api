import os
from flask import Flask, request
from flask_smorest import Api
import uuid
from resources.shop import blueprint as ShopBluePrint
from resources.product import blueprint as ProductBluePrint
from db import db
import models

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Shops REST API"
app.config["API_VERSION"] = "v1" 
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] =  "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] =  "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///shop.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

api = Api(app)

with app.app_context():
    db.create_all()

api.register_blueprint(ShopBluePrint)
api.register_blueprint(ProductBluePrint)