from data.__all_models import *
from flask import Blueprint, jsonify, request
from data import db_session

blueprint = Blueprint('films_api', __name__, template_folder='../templates')


@blueprint.route('/api/v1/films')
def get_films():
    session = db_session.create_session()
    films = session.query(Films).all()
    return jsonify({'films': [film.to_dict(only=('id', 'name', 'genre', 'year', 'description', 'image')) for film in films]})


@blueprint.route('/api/v1/films/<int:film_id>', methods=['GET'])
def get_one_film(film_id):
    session = db_session.create_session()
    film = session.query(Films).get(film_id)
    if not film:
        return jsonify({'error': 'film not found'})
    return jsonify({'films': film.to_dict(only=('id', 'name', 'genre', 'year', 'description', 'image'))})


@blueprint.route('/api/v1/films', methods=['POST'])
def create_film():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'empty request'})
    elif 'id' in request.json:
        return jsonify({'error': 'id in request'})
    elif not all(key in request.json for key in ['name', 'year', 'genre']):
        return jsonify({'error': 'not enough arguments'})
    film = Films(
        name=request.json['name'],
        genre=request.json['genre'],
        year=request.json['year']
    )
    if 'image' in request.json:
        film.image = request.json['image']
    if 'description' in request.json:
        film.description = request.json['description']
    session.add(film)
    session.commit()
    return jsonify({'success': 'film added'})


@blueprint.route('/api/v1/films/<int:film_id>', methods=['DELETE'])
def delete_film(film_id):
    session = db_session.create_session()
    film = session.query(Films).get(film_id)
    reviews = film.reviews
    if not film:
        return jsonify({'error': 'film not found'})
    if reviews:
        for review in reviews:
            session.delete(review)
    session.delete(film)
    session.commit()
    return jsonify({'success': 'film deleted'})


@blueprint.route('/api/v1/films/<int:film_id>', methods=['PUT'])
def edit_film(film_id):
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'empty request'})
    elif 'id' in request.json:
        return jsonify({'error': 'id in request'})
    elif not all(key in request.json for key in ['name', 'genre', 'year']):
        return jsonify({'error': 'not enough arguments'})
    film = session.query(Films).get(film_id)
    if not film:
        return jsonify({'error': 'film not found'})
    film.name = request.json['name']
    film.genre = request.json['genre']
    film.year = request.json['year']
    if 'image' in request.json:
        film.image = request.json['image']
    session.commit()
    return jsonify({'success': 'film edited'})


@blueprint.route('/api/v1/films/<int:film_id>/reviews')
def get_reviews(film_id):
    session = db_session.create_session()
    film = session.query(Reviews).get(film_id)
    if not film:
        return jsonify({'error': 'film not found'})
    reviews = film.reviews
    return jsonify({'reviews': [review.to_dict(only=('id', 'user_id', 'film_id', 'body')) for review in reviews]})
