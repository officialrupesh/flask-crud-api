from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import db
import uuid
from schemas import ProductSchema,ProductUpdateSchema
from models import ProductModel
from sqlalchemy.exc import SQLAlchemyError

blueprint  = Blueprint("products", __name__, description="Operations on Products")


@blueprint.route("/product")
class ProductList(MethodView):
    @blueprint.response(200, ProductSchema(many=True))
    def get(self):
        return ProductModel.query.all()

    @blueprint.arguments(ProductSchema)
    @blueprint.response(201,ProductSchema)
    def post(self, new_product ):
        product = ProductModel(**new_product)

        # for product in products.values():
        #     if(new_product["name"] == product["name"]
        #     and new_product["shop_id"] == product["shop_id"]):
        #         abort(400, message = "Product already exists") 
       
        # product_id = uuid.uuid4().hex
        # product = {**new_product, "id" : product_id}
        # products[product_id] = product

        try: 
            db.session.add(product)
            db.session.commit()

        except IntegrityError:
            abort(400, message="A product with that name already exists.")    
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the product")

        return product

@blueprint.route("/product/<product_id>")
class Product(MethodView):
    @blueprint.response(200, ProductSchema)
    def get(self,product_id):
            product = ProductModel.query.get_or_404(product_id)
            return product 
       
    @blueprint.arguments(ProductUpdateSchema)
    @blueprint.response(200, ProductSchema)
    def put(self,product_data, product_id):            
        product = ProductModel.query.get_or_404(product_id)
        if product:
            product.price = product_data.get("price", product.price)
            product.name = product_data.get("name", product.name)
        else:
            product = ProductModel(id=product_id, **product_data)
        try:
            db.session.add(product)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A product with that name already exists.")
        except SQLAlchemyError:
            abort(500, "Error while updating product")
        return product


    def delete(self,product_id):
        product = ProductModel.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted"}