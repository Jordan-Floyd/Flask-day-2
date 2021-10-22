from flask import Blueprint, request, jsonify
from car_inventory.helpers import token_required
from car_inventory.models import  Car, db, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix = '/api')


@api.route('/cars', methods = ['POST'])
@token_required

def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    color = request.json['color']
    max_speed = request.json['max_speed']
    doors = request.json['doors']
    horsepower = request.json['horsepower']
    token = current_user_token.token

    print(f'TEST: {current_user_token.token}')
    
    car = Car(make, model, color, max_speed, doors, horsepower, user_token = token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)



@api.route('/cars', methods = ['GET'])
@token_required

def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)



@api.route('/drones/<id>', methods = ['GET'])
@token_required

def get_car(current_user_token, id):
    car = Car.query.get(id)
    if car:
        print(f'Here is your Car: {car.name}')
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That Car does not exist'})



@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required

def update_car(current_user_token, id):
    car = Car.query.get(id)
    print(car)
    if car:
        car.make = request.json['make']
        car.model = request.json['model']
        car.color = request.json['color']
        car.max_speed = request.json['max_speed']
        car.doors = request.json['doors']
        car.horsepower = request.json['horsepower']
        car.user_token = current_user_token.token

        db.session.commit()
        response = car_schema.dump(car)

        return jsonify(response)
    else:
        return jsonify ({'Error': 'That car does not exist'})



@api.route('/cars/<id>', methods = ['DELETE'])
@token_required

def delete_car(current_user_token, id):
    car = Car.query.get(id)
    if car:
        db.session.delete(car)
        db.session.commit()
        return jsonify({'Success': f'Car ID #{car.id} has been deleted'})
    else:
        return jsonify({'Error': 'That car does not exist'})


