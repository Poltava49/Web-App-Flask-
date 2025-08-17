import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String,
                             nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String,
                             nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer,
                            nullable=True)
    position = sqlalchemy.Column(sqlalchemy.String,
                                 nullable=True)
    speciality = sqlalchemy.Column(sqlalchemy.String,
                                   nullable=True)
    adress = sqlalchemy.Column(sqlalchemy.String,
                                   nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String,
                                        nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    # jobs = orm.relationship("Jobs", back_populates='user')

    def __repr__(self):
        return f'<Colonist> {self.id} {self.surname} {self.name} {self.age} years, {self.speciality}'


