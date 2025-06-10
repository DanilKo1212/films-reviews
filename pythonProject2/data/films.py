from sqlalchemy import Column, Integer, String
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Films(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'films'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    year = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image = Column(String, default='defalut.png')