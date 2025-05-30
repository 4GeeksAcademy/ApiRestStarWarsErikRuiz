from flask import Blueprint, jsonify, request
from src.models import db, People, Planet, User, Favorite

api = Blueprint('api', __name__)

# PEOPLE CRUD
@api.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    return jsonify([{'id': p.id, 'name': p.name} for p in people])

@api.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get_or_404(people_id)
    return jsonify({'id': person.id, 'name': person.name})

@api.route('/people', methods=['POST'])
def create_person():
    data = request.get_json()
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    person = People(name=data['name'])
    db.session.add(person)
    db.session.commit()
    return jsonify({'msg': 'Person created', 'id': person.id}), 201

@api.route('/people/<int:people_id>', methods=['PUT'])
def update_person(people_id):
    data = request.get_json()
    person = People.query.get_or_404(people_id)
    person.name = data.get('name', person.name)
    db.session.commit()
    return jsonify({'msg': 'Person updated', 'id': person.id})

@api.route('/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):
    person = People.query.get_or_404(people_id)
    db.session.delete(person)
    db.session.commit()
    return jsonify({'msg': 'Person deleted'})

# PLANETS CRUD
@api.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([{'id': p.id, 'name': p.name} for p in planets])

@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    return jsonify({'id': planet.id, 'name': planet.name})

@api.route('/planets', methods=['POST'])
def create_planet():
    data = request.get_json()
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    planet = Planet(name=data['name'])
    db.session.add(planet)
    db.session.commit()
    return jsonify({'msg': 'Planet created', 'id': planet.id}), 201

@api.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    data = request.get_json()
    planet = Planet.query.get_or_404(planet_id)
    planet.name = data.get('name', planet.name)
    db.session.commit()
    return jsonify({'msg': 'Planet updated', 'id': planet.id})

@api.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    db.session.delete(planet)
    db.session.commit()
    return jsonify({'msg': 'Planet deleted'})

# USERS
@api.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username} for u in users])

# FAVORITES (Simula user_id=1)
@api.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    favorites = Favorite.query.filter_by(user_id=1).all()
    data = []
    for fav in favorites:
        if fav.people_id:
            person = People.query.get(fav.people_id)
            data.append({'type': 'people', 'id': person.id, 'name': person.name})
        if fav.planet_id:
            planet = Planet.query.get(fav.planet_id)
            data.append({'type': 'planet', 'id': planet.id, 'name': planet.name})
    return jsonify(data)

@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    new_fav = Favorite(user_id=1, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({'msg': 'Favorite planet added'})

@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    new_fav = Favorite(user_id=1, people_id=people_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({'msg': 'Favorite person added'})

@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    fav = Favorite.query.filter_by(user_id=1, planet_id=planet_id).first_or_404()
    db.session.delete(fav)
    db.session.commit()
    return jsonify({'msg': 'Favorite planet removed'})

@api.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    fav = Favorite.query.filter_by(user_id=1, people_id=people_id).first_or_404()
    db.session.delete(fav)
    db.session.commit()
    return jsonify({'msg': 'Favorite person removed'})