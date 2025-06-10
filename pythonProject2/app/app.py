import os.path

from requests import get

from data.__all_models import *
from flask import Flask, render_template
from flask_login import LoginManager
from flask_restful import Api
from api.v1 import users_api, films_api, reviews_api
from api.v2 import users_resource, films_resource, reviews_resource
from data import db_session
from films import add_films_routes
from users import add_user_routes

app = Flask(__name__, template_folder=os.path.abspath('../templates'), static_folder=os.path.abspath('../static'))
app.config['SECRET_KEY'] = 'secret'
db_session.global_init('../db/films.db')
session = db_session.create_session()
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
add_films_routes(app)
add_user_routes(app, session)


@login_manager.user_loader
def load_user(user_id):
    return session.query(Users).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    films = get('http://localhost:8080/api/v2/films').json()['films']
    return render_template('index.html', films=films)


if __name__ == '__main__':
    app.register_blueprint(films_api.blueprint)
    app.register_blueprint(reviews_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    api.add_resource(films_resource.FilmsListResource, '/api/v2/films')
    api.add_resource(films_resource.FilmsResource, '/api/v2/films/<int:film_id>')
    api.add_resource(films_resource.FilmsReviews, '/api/v2/films/<int:film_id>/reviews')
    api.add_resource(reviews_resource.ReviewsListResource, '/api/v2/reviews')
    api.add_resource(reviews_resource.ReviewsResource, '/api/v2/reviews/<int:review_id>')
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
    app.run(port=8080, host='localhost')
