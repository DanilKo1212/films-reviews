from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.__all_models import *
from api.v2.parser import ParserFilms

parser = ParserFilms()


def films_not_found(film_id):
    session = db_session.create_session()
    film = session.query(Films).get(film_id)
    if not film:
        abort(404, message=f'Film {film_id} not found')


class FilmsResource(Resource):
    def get(self, film_id):
        films_not_found(film_id)
        session = db_session.create_session()
        film = session.query(Films).get(film_id)
        return jsonify({'films': film.to_dict(only=('id', 'image', 'name', 'genre', 'year', 'description'))})

    def delete(self, film_id):
        films_not_found(film_id)
        session = db_session.create_session()
        film = session.query(Films).get(film_id)
        reviews = film.reviews
        if reviews:
            for review in reviews:
                session.delete(review)
        session.delete(film)
        session.commit()
        return jsonify({'success': f'Film {film_id} was deleted'})

    def put(self, film_id):
        args = parser.parse_args()
        films_not_found(film_id)
        session = db_session.create_session()
        film = session.query(Films).get(film_id)
        if 'name' in args:
            film.name = args['name']
        if 'year' in args:
            film.year = args['year']
        if 'genre' in args:
            film.genre = args['genre']
        if 'image' in args:
            film.image = args['image']
        if 'description' in args:
            film.description = args['description']
        session.commit()
        return jsonify({'success': 'film edited'})


class FilmsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        films = session.query(Films).all()
        return jsonify({'films': [film.to_dict(only=('id', 'image', 'name', 'genre', 'year', 'description')) for film in films]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if not all(key in args for key in ['name', 'genre', 'year']):
            return jsonify({'error': 'not enough arguments'})
        film = Films(
            name=args['name'],
            genre=args['genre'],
            year=args['year'],
        )
        if 'image' in args:
            film.image = args['image']
        if 'description' in args:
            film.description = args['description']
        session.add(film)
        session.commit()
        return jsonify({'success': 'film added'})


class FilmsReviews(Resource):
    def get(self, film_id):
        films_not_found(film_id)
        session = db_session.create_session()
        film = session.query(Films).get(film_id)
        reviews = film.reviews
        reviews_ = []
        for review in reviews:
            review = review.to_dict(only=('id', 'film_id', 'user_id', 'body'))
            user = session.query(Users).get(review['user_id'])
            review['user'] = user.login
            reviews_.append(review)
        print(reviews_)
        return jsonify({'reviews': reviews_})

