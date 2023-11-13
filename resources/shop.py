from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import db
import uuid
from schemas import ShopSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import ShopModel

blueprint  = Blueprint("shops", __name__, description="Operations on Shops")


@blueprint.route("/shop")
class ShopList(MethodView):
    @blueprint.response(200, ShopSchema(many=True))
    def get(self):
       return ShopModel.query.all()


    @blueprint.arguments(ShopSchema)
    @blueprint.response(201, ShopSchema)
    def post(self, shop_data):
        shop = ShopModel(**shop_data)
        try:
            db.session.add(shop)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "A shop with that name already exists")
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the product")
        return shop


@blueprint.route("/shop/<shop_id>")
class Shop(MethodView):
    @blueprint.response(200, ShopSchema)
    def get(self, shop_id):
        shop = ShopModel.query.get_or_404(shop_id)
        return shop
   
    def delete(self, shop_id):
        shop = ShopModel.query.get_or_404(shop_id)
        db.session.delete(shop)
        db.session.commit()
        return {"message": "Shop deleted"}
