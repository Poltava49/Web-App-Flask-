import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Department(SqlAlchemyBase):
    __tablename__ = 'department'
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    users = orm.relationship('User')


    def department_to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'chief': self.chief,
            'email': self.email
        }
