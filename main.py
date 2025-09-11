import login
from flask import Flask, render_template, url_for, request, redirect
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, RadioField, IntegerField, DateTimeField
from wtforms.fields.simple import EmailField
from wtforms.validators import DataRequired
from wtforms.widgets import ListWidget, CheckboxInput
from dotenv import load_dotenv
import os
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.department import Department
from data.db_session import global_init, create_session
from flask_login import login_user, current_user, login_required, logout_user


app = Flask(__name__)

load_dotenv()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


commands = [{'surname': 'Scott', 'name': 'Ridley', 'age': 21,
             'position': 'captain', 'speciality': 'research engineer', 'adress': 'module_1',
             'email':'scott_chief@mars.org'},
            {'surname': 'Malkovich', 'name': 'Tom', 'age': 45,
             'position': 'major', 'speciality': 'pilot', 'adress': 'module_2',
             'email':'tom_pilot@mars.org'},
            {'surname': 'Cage', 'name': 'Nicolas', 'age': 40,
             'position': 'major', 'speciality': 'actor', 'adress': 'module_3',
             'email':'nicolas_actor@mars.org'},
            {'surname': 'Hendricson', 'name': 'Richard', 'age': 25,
             'position': 'assistant', 'speciality': 'programmist', 'adress': 'module_4',
             'email':'richard_progt@mars.org'},
            {'surname': 'Harlesson', 'name': 'Rudy', 'age': 31,
             'position': 'ex-captain', 'speciality': 'junior research engineer', 'adress': 'module_1',
             'email': 'harly_chief@mars.org'}
            ]


new_commands = [{'surname': 'Kapoor', 'name': 'Venkat', 'age': 13,
             'position': 'middle', 'speciality': 'ML engineer', 'adress': 'module_2',
             'email':'vankat_ml@mars.org'},
            {'surname': 'Povarenok', 'name': 'Povar', 'age': 17,
             'position': 'chief', 'speciality': 'cooker', 'adress': 'module_3',
             'email': 'cooker_ml@mars.org'}
                ]


all_jobs = [{'team_leader': 7, 'jobs': 'Clean kitchen', 'work_size': 2,
             'collaborators': '3', 'is_finished': True},
            {'team_leader': 6, 'jobs': 'Created regression model for prognosis weather', 'work_size': 4,
             'collaborators': '1, 3', 'is_finished': False}]


new_departments = [{'title': 'geologic search', 'chief': 1, 'email': 'geologic_department@gmail.com'},
                   {'title': 'engineering division', 'chief': 2, 'email': 'engineering_department@gmail.com'},
                   {'title': 'kitchen division', 'chief': 3, 'email': 'kitchen_department@gmail.com'}
                   ]


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    repeat_password = PasswordField("Repeat password", validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    adress = StringField('Adress', validators=[DataRequired()])
    submit = SubmitField('Войти')


class ReLoginForm(FlaskForm):
    email = StringField('login/email', validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AccessForm(FlaskForm):
    astro_id = StringField('id астронавта', validators=[DataRequired()])
    password_astro = PasswordField('Пароль астронавта', validators=[DataRequired()])
    cap_id =StringField('id капитана', validators=[DataRequired()])
    cap_pass = PasswordField('Пароль капитана', validators=[DataRequired()])


class WorksForm(FlaskForm):
    team_leader = IntegerField('Руководитель', validators=[DataRequired()])
    jobs = StringField('Описание работы', validators=[DataRequired()])
    work_size = IntegerField('Объем работ в часах', validators=[DataRequired()])
    collaborators = StringField('Помощники', validators=[DataRequired()])
    end_date = DateTimeField('Дата завершения работы')
    is_finished = BooleanField('Статус работы')
    submit = SubmitField('Submit')


class EditWordForm(FlaskForm):
    team_leader = IntegerField('Руководитель', validators=[DataRequired()])
    jobs = StringField('Описание работы', validators=[DataRequired()])
    work_size = IntegerField('Объем работ в часах', validators=[DataRequired()])
    collaborators = StringField('Помощники', validators=[DataRequired()])
    end_date = DateTimeField('Дата завершения работы')
    is_finished = BooleanField('Статус работы')
    submit = SubmitField('Submit')


def add_department(new_departments):
    for i in range(len(new_departments)):
        department = Department()
        department.title = new_departments[i]['title']
        department.chief = new_departments[i]['chief']
        department.email = new_departments[i]['email']
        db_sess = db_session.create_session()
        db_sess.add(department)
        db_sess.commit()


def add_astro_pilot(commands):
    for i in range(len(commands)):
        user = User()
        user.surname = commands[i]['surname']
        user.name = commands[i]['name']
        user.age = commands[i]['age']
        user.position = commands[i]['position']
        user.speciality = commands[i]['speciality']
        user.adress = commands[i]['adress']
        user.email = commands[i]['email']
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()


def add_jobs(all_jobs):
    for i in range(len(all_jobs)):
        job = Jobs()
        job.team_leader = all_jobs[i]['team_leader']
        job.jobs = all_jobs[i]['jobs']
        job.work_size = all_jobs[i]['work_size']
        job.collaborators = all_jobs[i]['collaborators']
        job.is_finished = all_jobs[i]['is_finished']
        db_sess = db_session.create_session()
        db_sess.add(job)
        db_sess.commit()


def all_prompt():
    print('Для завершения пропиши команду End')
    db_name = input('Введите название базы данных ')
    try:
        global_init(f'db/{db_name}.db')
        db_sess = create_session()
    except Exception as e:
        print(f"\nОшибка: {e}\nПроверьте:")
        print(" Что файл базы существует и доступен")
        print(" Что существующая база имеет такое название")

    while db_name != 'End':
        try:
            global_init(f'db/{db_name}.db')
            db_sess = create_session()
            results = ''
            task = input('Какой запрос вывести? Пример: Запрос 1 ')
            if task =='Запрос 1':
                results = db_sess.query(User)
            elif task =='Запрос 2':
                results= db_sess.query(User).filter(User.adress == 'module_1')
            elif task =='Запрос 3':
                results= db_sess.query(User).filter(User.age < 18)
            elif task =='Запрос 4':
                results= db_sess.query(User).filter((User.position == 'chief') |(User.position == 'middle'))
            elif task =='Запрос 5':
                results= db_sess.query(Jobs).filter((Jobs.work_size < 20) & (Jobs.is_finished == 0))
                map(result.__repr__(), results)
            elif task =='Запрос 6':
                all_commands = db_sess.query(Jobs).filter(Jobs.collaborators).all()
                list_el = [(el.collaborators, el.user.surname, el.user.name) for el in all_commands]
                max_value = max(list_el, key=lambda item:len(item[0]))
                max_values_in_list = [x for x in list_el if len(x[0].split(',')) == len(max_value[0].split(','))]
                results =[' '.join([surname, name]) for string, surname, name in set(max_values_in_list)]
            elif task =='Запрос 7':
                results= db_sess.query(User).filter((User.adress == 'module_3') & (User.age < 21))
                for colonist in results:
                    colonist.adress = 'module_1'
                    db_sess.commit()
            elif task == 'Запрос 8':
                results = (db_sess.query(Jobs).join(User, User.id == Jobs.team_leader)
                           .join(Department, User.id == Department.chief)
                           .filter((Department.id==1) & (Jobs.is_finished == 1))
                           .all())
                for el in results:
                    print(el.user.name, el.user.surname)
            for result in results:
                print(result)
            else:
                raise Exception


        except Exception as e:
            print(f"\nОшибка: {e}\nПроверьте:")
            print("1. Что в базе есть нужная таблица")
            print("2. Что таблица содержит нужный столбец")
            print("4. Что такой запрос реализован в логике кода")


@app.route('/works_book')
def works_book():
    db_sess = create_session()
    form = db_sess.query(Jobs).all()
    return render_template('table_works_book.html', results=form, user=current_user)


@app.route('/works_book/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_work(id):
    form = WorksForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if jobs:  # Если работа найдена, заполняем форму данными
            form.team_leader.data = jobs.team_leader
            form.jobs.data = jobs.jobs
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.end_date.data = jobs.end_date
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
        # Если работа не найдена, форма останется пустой для создания новой

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if jobs:  # Если работа существует, обновляем её
            jobs.team_leader = form.team_leader.data
            jobs.jobs = form.jobs.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.end_date = form.end_date.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/works_book')
        else:
            abort(404)

    return render_template('work_form.html',
                           title='Редактирование работы',
                           form=form, user=current_user)


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/works_book')




@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/register',methods=['GET', 'POST'])
def register_form():
    form=RegisterForm()
    if form.validate_on_submit():
        user = User()
        user.name =form.name.data
        user.surname = form.surname.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.adress = form.adress.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/work_form', methods=['GET', 'POST'])
def add_work_form():
    form = WorksForm()
    if form.validate_on_submit():
        job = Jobs()
        job.team_leader = form.team_leader.data
        job.jobs = form.jobs.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.end = form.end_date.data
        job.is_finished = form.is_finished.data
        try:
            db_sess = db_session.create_session()
            db_sess.add(job)
            db_sess.commit()
            return redirect('/works_book')
        except Exception as e:
            print(f'Ошибка обработки формы работ - {e}')
    elif request.method == 'POST':
        print(f"Ошибки формы: {form.errors}")
    return render_template('work_form.html', title='Adding a job', form=form, user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = ReLoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            return redirect('/works_book')
        else:
            print('Неверный email или пароль', 'danger')
            # return render_template("success_enter.html", user_name=user.name)
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, user=current_user)
    return render_template('login.html', title='Авторизация', form=form)


def main():
    db_session.global_init("db/mars_explorer.db")
    # add_astro_pilot(new_commands)
    # add_jobs(all_jobs)
    # all_prompt()
    # works_book()
    # add_department(new_departments)


#Двойная защита
@app.route('/access', methods=['GET', 'POST'])
def access():
    form = AccessForm()
    if form.validate_on_submit():
        pass
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('base.html', title=title)



@app.route('/training/<prof>')
def prof_img(prof):
    if prof.lower().startswith('инженер') or prof.lower().startswith('строитель'):
        image_path = url_for('static', filename='img/ship2.webp')
        return render_template('profession.html', title=prof, image_path=image_path)
    else:
        image_path = url_for('static', filename='img/ship1.webp')
        return render_template('profession.html', title=prof, image_path=image_path)



@app.route('/list_prof/<type>')
def list_prof(type):
    tags = ['ul', 'ol']
    if type in tags:
        return render_template('list_prof.html',
                               tag=type)


@app.route('/distribution')
def choose_cabin():
    cabin = ['Denis', 'Dima', 'Sergey']
    return render_template('distribution.html',
                           list_cabin=cabin)


@app.route('/table/<sex>/<int:age>')
def cabin_decoration(sex, age):
    color = 'blue' if sex.lower() == 'male' else 'pink'
    img_file = 'kids.png' if age < 21 else 'adult.png'
    img_url = url_for('static', filename=f'img/{img_file}')

    return render_template(
        'cabin_decoration.html',
        color=color,
        img_url=img_url
    )


def astronaut_survey():
    if request.method == 'GET':
        return
    elif request.method == 'POST':
        print(request.form)
        return redirect('/answer')


@app.route('/')
def title():
    return f"<title>Миссия Колонизация Марса</title>"


@app.route('/promotion')
def promotion():
    return (f"<title>Рекламная кампания</title>"
            f"<strong>Человечество вырастает из детства</strong> <br>"
            f" <strong>Человечеству мала одна планета</strong> <br>"
            f"<strong>Мы сделаем обитаемыми безжизненные пока планеты</strong> <br>"
            f"<strong>И начнем с Марса!</strong> <br><strong>Присоединяйся!</strong> <br>")


@app.route('/image_mars')
def hello_mars():
    return (f'''<title>Привет, Марс!</title>'''
            f'''<h1>Жди нас, Марс!</h1>'''
            f'''<img src="{url_for('static', filename='img/mars.jpg')}"
           alt="здесь должна была быть картинка, но не нашлась">'''
            )


@app.route('/promotion_image')
def promoted_image():
    return (f'''
            <head>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css" rel="stylesheet"
                        integrity="sha384-LN+7fdVzj6u52u30Kp6M/trliBMCMKTyK833zpbD+pXdCLuTusPj697FH4R/5mcr" crossorigin="anonymous">
                        <title>Миссия Колонизация Марса</title>
                <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}"
           </head>
           <body>
           <h1>Жди нас, Марс!</h1>
            <div> <img src="{url_for('static', filename='img/mars.jpg')}"  alt="здесь должна была быть картинка, но не нашлась"></div>

            <title>Рекламная кампания</title>

            <div class="alert alert-primary" role="alert">
             Человечество вырастает из детства
            </div>
            <div class="alert alert-secondary" role="alert">
              Человечеству мала одна планета
            </div>
            <div class="alert alert-success" role="alert">
              A simple success alert—check it out!
            </div>
            <div class="alert alert-danger" role="alert">
              A simple danger alert—check it out!
            </div>
            <div class="alert alert-warning" role="alert">
              A simple warning alert—check it out!
            </div>
            <div class="alert alert-info" role="alert">
              A simple info alert—check it out!
            </div>
            <div class="alert alert-light" role="alert">
              A simple light alert—check it out!
            </div>
            <div class="alert alert-dark" role="alert">
              A simple dark alert—check it out!
            </div>
</body>''')


#Шаблон формы и автоматический ответ на анкету
@app.route('/answer', methods=["GET", "POST"])
def astronaut_survey():
    if request.method == 'GET':
        return f"""<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                            <title>Отбор астронавтов</title>
                            <style>
                            
                            </style>
                          </head>
                          <body>
                            <h1>Анкета претендента</h1>
                            <h2>на участие в миссии</h2>
                             <div class="form-group">
                                <form class="form-control" method="post" >
                                     <input name="surname" class="form-control" id="surname"  placeholder="Введите фамилию" > <br>
                                     <input name="name" class="form-control" placeholder="Введите имя"><br>
                                     <input name="email" class="form-control" placeholder="Введите адрес почты"><br>
                                    <label for="classSelect">Какое у Вас образование?</label>
                                    <select class="form-control" id="classSelect" name="class">
                                      <option>Начальное</option>
                                      <option>Среднее общеобразовательное</option>
                                      <option>Среднее профессиональное</option>
                                      <option>Высшее неполное</option>
                                      <option>Высшее полное</option>
                                    </select>
                                    <label for="form-group form-check">Какие у Вас есть профессии?</label>
                                    <div name = "prof_list" class="form-control form-check">
                                         
                                        <label class="form-check-label" ><input type="checkbox" name="profession" value="engineer" >Инженер-исследователь </label><br>
                                       
                                        <label class="form-check-label" name="profession" value="sub-engineer"> <input type="checkbox" name="profession" value="sub-engineer">Инженер-строитель</label><br>
                                        <input type="checkbox" name="profession">
                                        <label class="form-check-label" for="profession">Пилот</label><br>
                                        <input type="checkbox" name="profession">
                                        <label class="form-check-label" for="profession">Метеоролог</label><br>
                                        <input type="checkbox" name="profession">
                                        <label class="form-check-label" for="profession">Инженер по жизнеобеспечению</label><br>
                                        <input type="checkbox" name="profession">
                                        <label class="form-check-label" for="profession">Инженер по радиационной защите</label><br>
                                        <input type="checkbox" name="profession">
                                        <label class="form-check-label" for="profession">Врач</label><br>
                                        <input type="checkbox" name="profession">
                                        <label class="form-check-label" for="profession">Экзобиолог</label><br>
                                    </div>
                                    <div class="form-control">
                                    <label for="form-check">Укажите пол</label>
                                    <div class="form-control">
                                      <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                      <label class="form-check-label" for="male">
                                        Мужской
                                      </label>
                                    </div>
                                    <div class="form-control">
                                      <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                      <label class="form-check-label" for="female">
                                        Женский
                                      </label>
                                    </div>
                                    <div cclass="form-control">
                                    <label for="about">Почему Вы хотите принять участие в миссии?</label> </br>
                                    <textarea name="about" rows="3"></textarea>
                                    </div>
                                    <div class="form-control">
                                    <label for="photo">Приложите фотографию</label>
                                    <input type="file" class="form-control-file" id="photo" name="file">
                                    </div>
                                    <div class="form-control">
                                      <input type="radio" name="fin_question">
                                      <label for="fin_question">
                                        Готовы остаться на Марсе?
                                      </label>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Отправить</button>
                                </form>
                            </div>
                          </body>        
"""
    elif request.method == 'POST':
        print(request.form)
        print(request.form.values())
        return render_template('auto_answer.html', keys=list(request.form.values()), form = list(request.form.values()))


@app.route('/choice/<planet_name>')
def choise_planet(planet_name):
    if planet_name.lower() == "марс":
        return (f'''
            <head>
            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}">
            <title>Варианты выбора</title>
            </head>
            <h1> Мое предложение: {planet_name.capitalize()}</h1>
            <div> <img src="{url_for('static', filename='img/mars.png')}"  alt="здесь должна была быть картинка, но не нашлась"></div>
            <div id=grey_title>Эта планета близка к Земле"</div>
            <div id=red_title>На ней много необходимых ресурсов</div>
            <div id=green_title>На ней есть вода и атмосфера</div>
            <div id=yellow_title>На ней есть небольшое магнитное поле</div>
            <div id=green_title>Наконец, она просто красива!</div>''')
    elif planet_name == "юпитер":
        return (f'''
                <head>
                <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}">
                <title>Варианты выбора</title>
                </head>
                <body>
                    <h1> Мое предложение: {planet_name.capitalize()}</h1>
                    <div>
                        <div> <img src="{url_for('static', filename='img/yupiter.jpg')}"  alt="здесь должна была быть картинка, но не нашлась"></div>
                        <div id=grey_title>Эта планета далеко от Земли"</div>
                        <div id=green_title> На ней много необходимых ресурсов</div>
                        <div id=yellow_title>На ней есть вода и атмосфера</div>
                        <div id=red_title>На ней есть небольшое магнитное поле</div>
                        <div id=green_title>Наконец, она просто красива!</div>
                    </div>
                </body>''')


@app.route('/results/<nickname>/<int:level>/<float:rating>')
def astronaut_rating(nickname, level, rating):
    return f'''
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
        rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
        <title>
            Результаты
        </title>
    </head>
    <body>
        <h1> Результаты отбора</h1>
        <h2>Претендента на участие в миссии {nickname}:</h2>
        <h3 id=green_title>Поздравляем! Ваш рейтинг после {level} этапа отбора</h3>
        <h3>Составляет {rating}!</h3>
        <h3 id=yellow_title>Желаем удачи!</h3>
    </body>
    '''


@app.route('/carousel')
def carousel_planet():
    return f'''
    <head>
    <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
        integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
        crossorigin="anonymous">
        <title>Пейзажи Марса</title>
    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style_form.css')}" />
    </head>
    <body>
        <h1>Пейзажи Марса</h1>
        <div class="container mt-4">
            <div id="carouselExampleIndicators" class="carousel slide" data-bs-ride="carousel">
                <div class="carousel-inner">
                    <div class="carousel-item active">
                        <img src="{url_for('static', filename='img/mars_1.jpg')}" class="d-block w-100" alt="Фото 1">
                    </div>
                    <div class="carousel-item">
                        <img src="{url_for('static', filename='img/mars_2.jpg')}" class="d-block w-100" alt="Фото 2">
                    </div>
                    <div class="carousel-item">
                        <img src="{url_for('static', filename='img/mars_3.jpg')}" class="d-block w-100" alt="Фото 3">
                    </div>
                    <div class="carousel-item">
                        <img src="{url_for('static', filename='img/mars_4.jpg')}" class="d-block w-100" alt="Фото 3">
                    </div>
                    <div class="carousel-item">
                        <img src="{url_for('static', filename='img/mars_5.jpg')}" class="d-block w-100" alt="Фото 3">
                    </div>
                    <div class="carousel-item">
                        <img src="{url_for('static', filename='img/mars_6.jpg')}" class="d-block w-100" alt="Фото 3">
                    </div>
                    <div class="carousel-item">
                        <img src="{url_for('static', filename='img/mars_7.jpg')}" class="d-block w-100" alt="Фото 3">
                    </div>
                </div>
                <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Предыдущий</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Следующий</span>
                </button>
            </div>
        </div>
          <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js"
          crossorigin="anonymous"></script>
    </body>
    '''


# @app.route('/choose_astro')
# def get_picture():
#     return


if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1')
