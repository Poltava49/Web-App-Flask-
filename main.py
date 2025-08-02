from flask import Flask, render_template, url_for, request, redirect


app = Flask(__name__)


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



@app.route('/form', methods=["GET", "POST"])
def astronaut_survey():
    if request.method == 'GET':
        return
    elif request.method == 'POST':
        print(request.form)
        return redirect('/answer')




@app.route('/form/', methods=['GET', 'POST'])
def render_form():
    form = MyForm()
    if form.validate_on_submit():
        output = render_template('form-success.html', form=form)
        return output
    else:
        output = render_template('form.html', form=form)
        return output


@app.route('/answer')
def answer(forms):
    return render_template('auto_answer.html', forms = forms)
if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')