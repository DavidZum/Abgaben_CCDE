# Declarative-Variante wird hier benutzt
from flask import Flask, request,jsonify, render_template # SESSIONS
from sqlalchemy import Column, Integer, Text, Float, DateTime, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
from flask_restful import Resource, Api
from dataclasses import dataclass
import json
import random

Base = declarative_base()  # Basisklasse aller in SQLAlchemy verwendeten Klassen
metadata = Base.metadata

engine = create_engine('sqlite:///sqlalchemy\data\millionaire.sqlite3')
db_session = scoped_session(sessionmaker(autoflush=True, bind=engine))
db_session = scoped_session(sessionmaker(autoflush=True, bind=engine))
Base.query = db_session.query_property()

app = Flask(__name__)
api = Api(app)


@app.route('/')
def home():
    return render_template('home.html')

currentQuestion = None
currentDiff = 0

@app.route('/millionaire/')
def game():
    global currentQuestion
    global currentDiff
    currentQuestion = Question.query.filter(Question.difficulty == currentDiff).order_by(func.random()).first()
    answers = [currentQuestion.correct_answer, currentQuestion.answer2, currentQuestion.answer3, currentQuestion.answer4]
    random.shuffle(answers)
    return render_template('question.html', question=currentQuestion.question, 
                           answers=answers)

@app.route('/millionaire/submit/<string:answer>')
def submit(answer):
    global currentQuestion
    global currentDiff
    if currentQuestion.correct_answer == answer:
        currentDiff = currentDiff + 1
        answerStr = "Richtige Antwort!"
    else: 
        currentDiff = 1
        answerStr = "Falsche Antwort!"
    if currentDiff >= 5:
        currentDiff = 0
        answerStr = "Du hast gewonnen!"
    return render_template('next.html', answer=answerStr, level=currentDiff)

    

@dataclass
class Question(Base):
    __tablename__ = 'millionaire'
    
    id: int
    difficulty: int
    question: str
    correct_answer: str
    answer2: str
    answer3: str
    answer4: str

    id = Column(Integer, primary_key=True)
    difficulty = Column(Integer)
    question = Column(Text)
    correct_answer = Column(Text)
    answer2 = Column(Text)
    answer3 = Column(Text)
    answer4 = Column(Text)
    
class MillionaireREST(Resource):
    def get(self, id):
        q = Question.query.get(id)
        return jsonify(q)
    
    def put(self, id):
        global questions
        data = request.get_json(force=True)
        questions.append(Question(id, data['level'], data['frage'], data['antworten'], data['richtig']))
        print("put")
        return {"Message": "%s gespeichert" % id}

    def delete(self, id):
        db_session.delete(id)
        db_session.flush()
        return {"Message": "%s gelöscht" % id}

    def patch(self, id):
        global questions
        data = request.get_json(force=True)
        q = Question.query.get(id)
        print('patch')
        print(data)
        if 'difficulty' in data:
            q.difficulty = data['difficulty']
        if 'question' in data:
            q.question = data['question']
        if 'correct_answer' in data:
            q.correct_answer = data['correct_answer']
        if 'answer2' in data:
            q.answer2 = data['answer2']
        if 'answer3' in data:
            q.answer3 = data['answer3']
        if 'answer4' in data:
            q.answer4 = data['answer4']
        db_session.add(q)
        db_session.flush()
        return {"Message": "%d gepatched" % id}
    
    
api.add_resource(MillionaireREST, '/millionaire/question/<int:id>')

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)