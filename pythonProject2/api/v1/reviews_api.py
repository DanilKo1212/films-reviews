from data import db_session
from data.__all_models import *
from flask import Blueprint, jsonify, request

blueprint = Blueprint('reviews_api', __name__, template_folder='../templates')


@blueprint.route('/api/v1/reviews', methods=['GET'])
def get_reviews_all():
    session = db_session.create_session()
    reviews = session.query(Reviews).all()
    return jsonify({'reviews': [review.to_dict(only=('id', 'user_id', 'film_id', 'body')) for review in reviews]})


@blueprint.route('/api/v1/reviews/<int:review_id>', methods=['GET'])
def get_one_review(review_id):
    session = db_session.create_session()
    review = session.query(Reviews).get(review_id)
    if not review:
        return jsonify({'error': 'review not found'})
    return jsonify({'reviews': review.to_dict(only=('id', 'user_id', 'film_id', 'body'))})


@blueprint.route('/api/v1/reviews', methods=['POST'])
def create_review():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'empty request'})
    elif 'id' in request.json:
        return jsonify({'error': 'id in request'})
    elif not all(key in request.json for key in ['user_id', 'film_id', 'body']):
        return jsonify({'error': 'not enough arguments'})
    review = Reviews(
        user_id=request.json['user_id'],
        film_id=request.json['film_id'],
        body=request.json['body']
    )
    session.add(review)
    session.commit()
    return jsonify({'success': 'review added'})


@blueprint.route('/api/v1/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    session = db_session.create_session()
    review = session.query(Reviews).get(review_id)
    if not review:
        return jsonify({'error': 'review not found'})
    session.delete(review)
    session.commit()
    return jsonify({'success': 'review deleted'})


@blueprint.route('/api/v1/reviews/<int:review_id>', methods=['PUT'])
def edit_review(review_id):
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'empty request'})
    elif 'id' in request.json:
        return jsonify({'error': 'id in request'})
    elif not all(key in request.json for key in ['user_id', 'film_id', 'body']):
        return jsonify({'error': 'not enough arguments'})
    review = session.query(Reviews).get(review_id)
    review.user_id = request.json['user_id']
    review.film_id = request.json['film_id']
    review.body = request.json['body']
    session.commit()
    return jsonify({'success': 'review edited'})
