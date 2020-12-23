from dataclasses import dataclass
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
import requests

from producer import publish

app = Flask(__name__)
                                        #databaseType://user:password@host/databasename
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@db/main"
CORS(app=app)

db=SQLAlchemy(app)

@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    
    UniqueConstraint("user_id", "product_id", name="user_product_unique") #this will make sure the combination of product_
                                                                         # id and user_id should be unique should not be the same

@app.route("/api/products")
def index():
    return jsonify(Product.query.all())

@app.route("/api/products/<int:id>/like", methods=["POST"])
def like(id):
    req = requests.get('http://docker.for.linux.localhost:8000/api/user')
    json  = req.json()
    print(req, json)
    try:
        productUser = ProductUser(user_id=json["id"], product_id=id)
        db.session.add(productUser)
        db.session.commit()
        publish("product_liked", id)
    except Exception as e:
        print("error is ", e, json)
        abort(400, "you already liked this product")
    return jsonify({"message" : "success"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')    