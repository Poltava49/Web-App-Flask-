import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Jobs(SqlAlchemyBase):
    __tableName__ = 'jobs'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           autoincrement=True)
    team_leader =sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    jobs = sqlalchemy.Column(sqlalchemy.String,
                             nullable=True)
    work_size = datetime.datetime.hour
    collaborators = sqlalchemy.Column(sqlalchemy.String,
                                      nullable=True)
    start_date = datetime.datetime.now
    end_date = sqlalchemy.Column(sqlalchemy.DateTime)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean)
    user = orm.relationship('User')