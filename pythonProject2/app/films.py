from flask import request, redirect, render_template
from flask_login import login_required, current_user
from requests import get, put, post, delete
from werkzeug.utils import secure_filename
from forms.films import EditFilmsForm
from forms.reviews import EditReviewForm


def add_films_routes(app):
    @app.route('/films/d/<int:film_id>', methods=['GET', 'POST'])
    def film_description(film_id):
        film = get(f'http://localhost:8080/api/v2/films/{film_id}').json()['films']
        reviews = get(f'http://localhost:8080/api/v2/films/{film_id}/reviews').json()['reviews']
        form = EditReviewForm()
        if form.validate_on_submit():
            review_add = post('http://localhost:8080/api/v2/reviews',
                              json={'user_id': current_user.id, 'film_id': film_id,
                                    'body': form.body.data}).json()
            if 'success' in review_add:
                return redirect(f'/films/d/{film_id}')
            return render_template('film_description.html', form=form, film=film, reviews=reviews, message=review_add)
        return render_template('film_description.html', form=form, film=film, reviews=reviews)

    @app.route('/delete/review/<int:review_id>', methods=['GET', 'POST'])
    @login_required
    def delete_review(review_id):
        review = get(f'http://localhost:8080/api/v2/reviews/{review_id}').json()['reviews']
        film_id = review['film_id']
        if current_user.is_admin or current_user.id == review['user_id']:
            review_del = delete(f'http://localhost:8080/api/v2/reviews/{review_id}').json()
            if 'success' in review_del:
                return redirect(f'/films/d/{film_id}')
        return redirect(f'/films/d/{film_id}')

    @app.route('/films/<int:film_id>', methods=['GET', 'POST'])
    @login_required
    def edit_film(film_id):
        film = get(f'http://localhost:8080/api/v2/films/{film_id}').json()['films']
        form = EditFilmsForm()
        if current_user.is_admin:
            if request.method == 'GET':
                form.name.data = film['name']
                form.genre.data = film['genre']
                form.year.data = film['year']
                form.description.data = film['description']
                form.image.data = film['image']
            if form.validate_on_submit():
                if form.image.data:
                    filename = secure_filename(form.image.data.filename)
                    form.image.data.save('../static/images/' + filename)
                else:
                    filename = film['image']
                film_update = put(f'http://localhost:8080/api/v2/films/{film_id}',
                                  json={'name': form.name.data, 'genre': form.genre.data,
                                        'year': form.year.data, 'description': form.description.data,
                                        'image': filename}).json()
                if 'success' in film_update:
                    return redirect(f'/films/d/{film_id}')
                else:
                    return render_template('edit_film.html', form=form, message=film_update)
        return render_template('edit_film.html', form=form)

    @app.route('/add/films', methods=['GET', 'POST'])
    @login_required
    def add_film():
        form = EditFilmsForm()
        if current_user.is_admin:
            if form.validate_on_submit():
                if form.image.data:
                    filename = secure_filename(form.image.data.filename)
                    form.image.data.save('../static/images/' + filename)
                else:
                    filename = 'default.png'
                film_add = post(f'http://localhost:8080/api/v2/films',
                                json={'name': form.name.data, 'genre': form.genre.data,
                                      'year': form.year.data, 'description': form.description.data,
                                      'image': filename}).json()
                if 'success' in film_add:
                    return redirect('/')
                else:
                    return render_template('edit_film.html', form=form, message=film_add)
        return render_template('edit_film.html', form=form)

    @app.route('/delete/films/<int:film_id>', methods=['GET', 'POST'])
    @login_required
    def delete_film(film_id):
        if current_user.is_admin:
            film_delete = delete(f'http://localhost:8080/api/v2/films/{film_id}').json()
            if 'success' in film_delete:
                return redirect('/')
        return redirect('/')
