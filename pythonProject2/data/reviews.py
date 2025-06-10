from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from data.db_session import SqlAlchemyBase


class Reviews(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    film_id = Column(Integer, ForeignKey('films.id'), nullable=False)
    body = Column(String, nullable=False)
    user = relationship('Users', backref='reviews')
    film = relationship('Films', backref='reviews')
