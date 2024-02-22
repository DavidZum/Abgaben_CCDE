from flask import Flask, request,jsonify
from flask_restful import Resource, Api
from dataclasses import dataclass
import random

@dataclass
class Question:
    _id: int
    _level: int
    _frage: str
    _antworten: [str]
    _richtig: int
    
    def __init__(self, id: int, level: int, frage: str, antworten: [str], richtig: int):
        self._id = id
        self._level = int(level)
        self._frage = frage
        self._antworten = antworten
        self._richtig = richtig

        richtigeAntwort = self._antworten[self._richtig]
        random.shuffle(self._antworten)
        self._richtig = self._antworten.index(richtigeAntwort) + 1


    def __str__(self):
        return f"Your current level is {self._level}!\n{self._frage}\n(0) {self._antworten[0]}\n(1) {self._antworten[1]}\n(2) {self._antworten[2]}\n(3) {self._antworten[3]}\n"

     
def lineToQuestion(line, id):
    parts = line.split("\t")
    return Question(id, parts[0], parts[1], [parts[2], parts[3], parts[4], str(parts[5]).removesuffix("\n")], 0)

def getQuestions():
    datei = open("REST_millionaire/data/millionaire.txt", "r")
    datei.readline()
    lines = datei.readlines()
    questions = []
    i = 1
    for line in lines:
        questions.append(lineToQuestion(line, i))
        i += 1
    return questions

questions = []

app = Flask(__name__)
api = Api(app)

class QuestionService(Resource):
    
    def get(self, id):
        print("get")
        for question in questions:
            if question._id == id:
                return jsonify(question)
        return {"Message" : "%s not found" % id}

    def put(self, id):
        global questions
        data = request.get_json(force=True)
        questions.append(Question(id, data['level'], data['frage'], data['antworten'], data['richtig']))
        print("put")
        return {"Message": "%s gespeichert" % id}

    def delete(self, id):
        for question in questions:
            if question._id == id:
                questions.remove(question)
                break
        return {"Message": "%s gelöscht" % id}

    def patch(self, id):
        global questions
        data = request.get_json(force=True)
        print('patch')
        print(data)
        for question in questions:
            if question._id == id:
                if 'level' in data:
                    question._level = data['level']
                if 'frage' in data:
                    question._frage = data['frage']
                if 'antwort' in data:
                    question._antwort = data['antwort']
                if 'richtig' in data:
                    question._richtig = data['richtig']
                break
        return {"Message": "%d gepatched" % id}
    
api.add_resource(QuestionService, '/millionaire/<int:id>')

class MillionaireService(Resource):
    def get(self):
        return jsonify(questions[random.randint(0, len(questions) - 1)])
    
api.add_resource(MillionaireService, '/millionaire/random_question')

if __name__ == '__main__':
    questions = getQuestions()
    app.run(debug=True)