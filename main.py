from flask import Flask, render_template, url_for, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, RadioField
from wtforms.fields.simple import EmailField
from wtforms.validators import DataRequired
from wtforms.widgets import ListWidget, CheckboxInput


app = Flask(__name__)

app.config['SECRET_KEY'] = '123'


# class MultiCheckboxField(SelectMultipleField):
#     widget = ListWidget(prefix_label=False)
#     option_widget = CheckboxInput()
#
#
# class LoginForm(FlaskForm):
#     name = StringField('Имя', validators=[DataRequired()])
#     name = StringField('Фамилия', validators=[DataRequired()])
#     password = EmailField("Email: ", validators=[DataRequired()])
#     remember_me = BooleanField('Запомнить меня')
#     submit = SubmitField('Войти')
#
#
# class OrderForm(FlaskForm):
#     graduation = SelectField('Образование', choices=[
#         ('first', 'Среднее общеобразовательное'),
#         ('first_prof', 'Среднее профессиональное'),
#         ('high_first', 'Высшее неполное'),
#         ('high_second', 'Высшее полное')
#     ])
#
# class InterestsForm(FlaskForm):
#     interests = MultiCheckboxField('Ваши интересы', choices=[
#         ('engineer', 'Инженер-исследователь'),
#         ('build', 'Инженер-строитель'),
#         ('pilot', 'Пилот'),
#         ('meteo', 'Метеоролог'),
#         ('life', 'Инженер по жизнеобеспечению'),
#         ('radio', 'Инженер по радиационной защите'),
#         ('doctor', 'Врач'),
#         ('biologist', 'Экзобиолог')
#     ])


# class GenderForm(FlaskForm):
#     gender = RadioField('Ваш пол',
#                       choices=[('male', 'Мужской'), ('female', 'Женский')],
#                       validators=[DataRequired(message="Выберите пол")])



class AccessForm(FlaskForm):
    astro_id = StringField('id астронавта', validators=[DataRequired()])
    password_astro = PasswordField('Пароль астронавта', validators=[DataRequired()])
    cap_id =StringField('id капитана', validators=[DataRequired()])
    cap_pass = PasswordField('Пароль капитана', validators=[DataRequired()])


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
        return render_template('list_prof.html', tag=type)



# @app.route('/form', methods=["GET", "POST"])
# def login():
#     if request.method == 'GET':
#         form_login = LoginForm()
#         form_order = MultiCheckboxField()
#         form_inter = InterestsForm()
#         form_list = MultiCheckboxField()
#         sex_form = GenderForm()
#         return redirect('/success')
#         # return render_template('login.html', title='Авторизация', form=form)



def astronaut_survey():
    if request.method == 'GET':
        return
    elif request.method == 'POST':
        print(request.form)
        return redirect('/answer')


@app.route('/answer')
def answer(forms):
    return render_template('auto_answer.html', forms = forms)


@app.route('/')
def title():
    return f"<title>Миссия Колонизация Марса</title>"

#
# @app.route('/index')
# def index():
#     return f"<title>Миссия Колонизация Марса</title><h1>И на Марсе будут яблони цвести!</h1>"


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

@app.route('/form', methods=["GET", "POST"])
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
                                    <div name = prof_list class="form-control" form-check">
                                        <input type="checkbox" name="profession"> 
                                        <label class="form-check-label" name=""profession"  value="Инженер-исследователь">Инженер-исследователь</label><br>
                                        <input type="checkbox" name="profession value="designer">
                                        <label class="form-check-label" for="profession">Инженер-строитель</label><br>
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
        print(request.form.values())
        return render_template('auto_answer.html', keys=list(request.form.values()), form = list(request.form.values()))




#


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
    app.run(port=8080, host='127.0.0.1')
