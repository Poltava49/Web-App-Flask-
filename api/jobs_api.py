import flask
from flask import abort
from data import db_session
from data import jobs
from data.jobs import Jobs
from flask import jsonify
import requests
from flask import request


blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs': [job.job_to_dict() for job in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        abort(404)
    return jsonify(
            {
                'job': [job.job_to_dict()]
            }
        )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    keys_list = ['id', 'team_leader','jobs', 'work_size',
                 'collaborators','start_date','is_finished']

    if not request.get_json():
        abort(415)

    if not request.json:
        abort(404)

    if not all([key in request.json for key in keys_list]):
        abort(404)

    db_sess = db_session.create_session()
    # Проверяем, существует ли уже работа с таким ID
    existing_job = db_sess.query(Jobs).filter(Jobs.id == request.json['id']).first()
    if existing_job:
        abort(404)  # Работа с таким ID уже существует
    job = Jobs(
        team_leader = request.json['team_leader'],
        jobs = request.json['jobs'],
        work_size = request.json['work_size'],
        collaborators=request.json['collaborators'],
        # start_date=request.json['start_date'],
        # end_date=request.json['end_date'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(job)
    db_sess.commit()
    return jsonify(
            {
                'status': 'OK'
            }
        )


@blueprint.route('/api/delete_job/<int:id>', methods=['DELETE'])
def delete_job(id):
    db_sess = db_session.create_session()
    if id is None:
        print(id)
        abort(415)
    job = db_sess.query(Jobs).get(id)
    if not job:
        abort(404)
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({
        'status': 200
    })



@blueprint.route('/api/edit_job/<int:id>', methods=['PUT'])
def edit_job(id):
    db_sess = db_session.create_session()
    if not isinstance(id,int) or id is None:
        abort(415)
    job = db_sess.query(Jobs).get(id)
    if not job:
        abort(404)
    if not request.json:
        abort(404)
    update_data = request.json
    print(job)
    job.team_leader = update_data['team_leader']
    job.jobs = update_data['jobs']
    job.work_size = update_data['work_size']
    job.collaborators = update_data['collaborators']
    job.is_finished = update_data['is_finished']
    db_sess.commit()
    return jsonify({
        'status': 200
    })





