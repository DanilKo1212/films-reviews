from flask_restful.reqparse import RequestParser


class ParserUsers(RequestParser):
    def __init__(self):
        super().__init__()
        self.add_argument('email', required=False)
        self.add_argument('login', required=False)
        self.add_argument('password', required=False)
        self.add_argument('is_admin', required=False)


class ParserFilms(RequestParser):
    def __init__(self):
        super().__init__()
        self.add_argument('name', required=True)
        self.add_argument('year', required=True)
        self.add_argument('genre', required=True)
        self.add_argument('image', required=False)
        self.add_argument('description', required=False)


class ParserReviews(RequestParser):
    def __init__(self):
        super().__init__()
        self.add_argument('film_id', required=True)
        self.add_argument('user_id', required=True)
        self.add_argument('body', required=True)
