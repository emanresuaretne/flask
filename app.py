from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.app = app
db.init_app(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/statistics')
def statistics():
    info = {}
    age_stats = db.session.query(
        func.avg(models.Person.age),
        func.min(models.Person.age),
        func.max(models.Person.age)
    ).one()
    info['age_mean'] = age_stats[0]
    info['age_min'] = age_stats[1]
    info['age_max'] = age_stats[2]
    info['total_count'] = models.Person.query.count()
    info['mood_mean'] = db.session.query(func.avg(models.Answer.mood)).one()[0]
    info['madmen'] = db.session.query(models.Answer).filter(models.Answer.colour == 'blue').count()
    return render_template("statistics.html", info=info)


@app.route('/inquiry', methods=['get'])
def get_inquiry():
    return render_template('inquiry.html')


@app.route('/inquiry', methods=['post'])
def post_inquiry():
    person = models.Person(
        gender=request.form.get('gender'),
        name=request.form.get('name'),
        age=request.form.get('age'),
    )
    db.session.add(person)
    db.session.commit()
    db.session.refresh(person)
    answer = models.Answer(
        person_id=person.person_id,
        number=request.form.get('number'),
        colour=request.form.get('colour'),
        mood=request.form.get('mood'),
    )
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)