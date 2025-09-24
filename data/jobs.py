import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    team_leader =sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    jobs = sqlalchemy.Column(sqlalchemy.String,
                             nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    collaborators = sqlalchemy.Column(sqlalchemy.String,
                                      nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    # end_date = sqlalchemy.Column(sqlalchemy.DateTime)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean)
    user = orm.relationship('User')


    def __repr__(self):
        return f'<Job> {self.jobs}'

    def job_to_dict(self):
        print("=== TYPES ===")
        print(f"id: {type(self.id)}")
        print(f"team_leader: {type(self.team_leader)}")
        print(f"jobs: {type(self.jobs)}")
        print(f"work_size: {type(self.work_size)}")
        print(f"collaborators: {type(self.collaborators)}")
        print(f"start_date: {type(self.start_date)}")
        # print(f"end_date: {type(self.end_date)}")
        print(f"is_finished: {type(self.is_finished)}")

        return {
            'id': self.id,
            'team_leader': self.team_leader,
            'jobs': self.jobs,
            'work_size': self.work_size,
            'collaborators': self.collaborators,
            'start_date': self.start_date,
            # 'end_date': self.end_date,
            'is_finished': self.is_finished
        }