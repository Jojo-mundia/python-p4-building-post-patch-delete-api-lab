#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# HOME ROUTE
@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

# GET all bakeries
@app.route('/bakeries', methods=['GET'])
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(jsonify(bakeries), 200)

# GET bakery by ID
@app.route('/bakeries/<int:id>', methods=['GET'])
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    return make_response(jsonify(bakery.to_dict()), 200)

# GET baked goods sorted by price descending
@app.route('/baked_goods/by_price', methods=['GET'])
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_serialized = [bg.to_dict() for bg in baked_goods]
    return make_response(jsonify(baked_goods_serialized), 200)

# GET the most expensive baked good
@app.route('/baked_goods/most_expensive', methods=['GET'])
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return make_response(jsonify(most_expensive.to_dict()), 200)

# POST a new baked good
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    name = request.form.get('name')
    price = request.form.get('price')
    bakery_id = request.form.get('bakery_id')

    if not name or not price or not bakery_id:
        return make_response({"error": "name, price, and bakery_id are required"}, 400)

    new_baked_good = BakedGood(name=name, price=float(price), bakery_id=int(bakery_id))
    db.session.add(new_baked_good)
    db.session.commit()
    return make_response(jsonify(new_baked_good.to_dict()), 201)

# PATCH a bakery name
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    name = request.form.get('name')

    if not name:
        return make_response({"error": "name is required to update"}, 400)

    bakery.name = name
    db.session.commit()
    return make_response(jsonify(bakery.to_dict()), 200)

# DELETE a baked good
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get_or_404(id)
    db.session.delete(baked_good)
    db.session.commit()
    return make_response({"message": f"Baked good {id} deleted successfully"}, 200)

# PATCH a baked good (update name or price)
@app.route('/baked_goods/<int:id>', methods=['PATCH'])
def update_baked_good(id):
    baked_good = BakedGood.query.get_or_404(id)
    name = request.form.get('name')
    price = request.form.get('price')

    if name:
        baked_good.name = name
    if price:
        baked_good.price = float(price)

    db.session.commit()
    return make_response(jsonify(baked_good.to_dict()), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
