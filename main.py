from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func, ForeignKey
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.app = app
db.init_app(app)


class Answer(db.Model):
    __tablename__ = "answers"

    # имя колонки = специальный тип (тип данных, первичный ключ)
    answer_id = db.Column('answer_id', db.Integer, primary_key=True)

    # соединяем
    person_id = db.Column('person_id', db.Integer, ForeignKey('persons.person_id'))
    number = db.Column('number', db.Integer)
    colour = db.Column('colour', db.Integer)
    mood = db.Column('mood', db.Integer)


class Question(db.Model):
    __tablename__ = "questions"
    question_id = db.Column('id', db.Integer, primary_key=True)
    question = db.Column('question', db.Text)


class Person(db.Model):
    __tablename__ = "persons"
    person_id = db.Column('person_id', db.Integer, primary_key=True)
    gender = db.Column('gender', db.Integer)
    name = db.Column('name', db.Text)
    age = db.Column('age', db.Text)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/statistics')
def statistics():
    info = {}
    age_stats = db.session.query(
        func.avg(Person.age),
        func.min(Person.age),
        func.max(Person.age)
    ).one()
    info['age_mean'] = age_stats[0]
    info['age_min'] = age_stats[1]
    info['age_max'] = age_stats[2]
    info['total_count'] = Person.query.count()
    info['mood_mean'] = db.session.query(func.avg(Answer.mood)).one()[0]
    info['madmen'] = db.session.query(Answer).filter(Answer.colour == 'blue').count()
    return render_template("statistics.html", info=info)


@app.route('/inquiry', methods=['get'])
def get_inquiry():
    return render_template('inquiry.html')


@app.route('/inquiry', methods=['post'])
def post_inquiry():
    person = Person(
        gender=request.form.get('gender'),
        name=request.form.get('name'),
        age=request.form.get('age'),
    )
    db.session.add(person)
    db.session.commit()
    db.session.refresh(person)
    answer = Answer(
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