from sqlalchemy import ForeignKey
from main import db


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
