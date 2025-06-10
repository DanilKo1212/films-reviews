from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.__all_models import *
from api.v2.parser import ParserReviews

parser = ParserReviews()


def reviews_not_found(review_id):
    session = db_session.create_session()
    review = session.query(Reviews).get(review_id)
    if not review:
        abort(404, message=f'Review {review_id} not found')


class ReviewsResource(Resource):
    def get(self, review_id):
        reviews_not_found(review_id)
        session = db_session.create_session()
        review = session.query(Reviews).get(review_id)
        return jsonify({'reviews': review.to_dict(only=('id','film_id', 'user_id', 'body'))})

    def delete(self, review_id):
        reviews_not_found(review_id)
        session = db_session.create_session()
        review = session.query(Reviews).get(review_id)
        session.delete(review)
        session.commit()
        return jsonify({'success': f'Review {review_id} was deleted'})

    def put(self, review_id):
        args = parser.parse_args()
        reviews_not_found(review_id)
        session = db_session.create_session()
        review = session.query(Reviews).get(review_id)
        if 'user_id' in args:
            review.user_id = args['user_id']
        if 'film_id' in args:
            review.film_id = args['film_id']
        if 'body' in args:
            review.body = args['body']
        session.commit()
        return jsonify({'success': 'review edited'})


class ReviewsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        reviews = session.query(Reviews).all()
        return jsonify({'reviews': [review.to_dict(only=('id','film_id', 'user_id', 'body')) for review in reviews]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if not all(key in args for key in ['user_id', 'film_id', 'body']):
            return jsonify({'error': 'not enough arguments'})
        review = Reviews(
            user_id=args['user_id'],
            film_id=args['film_id'],
            body=args['body']
        )
        session.add(review)
        session.commit()
        return jsonify({'success': 'review added'})
