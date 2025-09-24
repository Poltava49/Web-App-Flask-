import datetime

from requests import get, post, delete, put

def test_get_jobs():
    response = get('http://127.0.0.1:5000/api/jobs')
    print(response.content)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_job(id):
    response = get(f'http://127.0.0.1:5000/api/jobs/{id}')
    print(response.content)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_uncorrect_job(id):
    response = get(f'http://127.0.0.1:5000/api/jobs/{id}')
    assert response.status_code == 404


def test_create_job():
    tests_work = [
        {
            'id': 19, 'team_leader': 3, 'jobs': 'Create base data', 'work_size': 23,
            'collaborators': '3', 'start_date': datetime.datetime.now().isoformat(), 'end_date': None, 'is_finished': False
        },
        {
            'id': 1, 'team_leader': 3, 'jobs': 'Create base data', 'work_size': 22,
            'collaborators': '3', 'start_date': datetime.datetime.now().isoformat(), 'end_date': None, 'is_finished': False
        },
        None
    ]
    # Тест 1: Создание новой работы (должен вернуть 200)
    response1 = post(url=f'http://127.0.0.1:5000/api/jobs', json=tests_work[0])
    assert response1.status_code == 200

    # Тест 2: Попытка создать работу с существующим ID (должен вернуть 404)
    response2 = post(url=f'http://127.0.0.1:5000/api/jobs', json=tests_work[1])
    assert response2.status_code == 404

    # Тест 3: Передаем None вместо словаря (должен вернуть 415)
    response3 = post(url=f'http://127.0.0.1:5000/api/jobs', json=tests_work[2])
    assert response3.status_code == 415


def test_job_delete():
    tests = [5, 20, None, 'str']
    # #Тест 1: Проверка корретного типа и существующей работы
    # responce = delete(url=f'http://127.0.0.1:5000/api/delete_job/{tests[0]}')
    # print(responce.content)
    # assert responce.status_code == 200

    # Тест 2: Проверка корретного типа и несуществующей работы
    responce = delete(url=f'http://127.0.0.1:5000/api/delete_job/{tests[1]}')
    print(responce.content)
    assert responce.status_code == 404

    # Тест 3: Проверка на None
    responce = delete(url=f'http://127.0.0.1:5000/api/delete_job/{tests[2]}')
    print(responce.content)
    assert responce.status_code == 404

    # Тест 4: Проверка некорретного типа
    responce = delete(url=f'http://127.0.0.1:5000/api/delete_job/{tests[3]}')
    print(responce.content)
    assert responce.status_code == 404


def test_edit_job():
    update_jobs = [
        {
            'team_leader': 2, 'jobs': 'Create base data', 'work_size': 1,
            'collaborators': '1',
            'is_finished': False
        },
        {
            'team_leader': 3, 'jobs': 'Create base data', 'work_size': 22,
            'collaborators': '3',
            'is_finished': False
        },
    ]
    response = put(url=f'http://127.0.0.1:5000/api/edit_job/{2}', json=update_jobs[0])
    print(response.content)
    assert response.status_code == 200




# test_create_job()
#
# test_uncorrect_job('str')
#
# test_uncorrect_job(99)
#
# test_get_job(1)
#
# test_get_jobs()

# test_job_delete()

test_edit_job()