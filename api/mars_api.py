import flask
from data import db_session
from data import jobs



blueprint = flask.Blueprint(
    'mars_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/jobs')
def get_jobs():
    return 'Джобы не выбраны'