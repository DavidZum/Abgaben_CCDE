from flask import Flask, render_template
import random

class Question:
    
    def __init__(self, level, frage, antworten, richtig):
        self._level = level
        self._frage = frage
        self._antworten = antworten
        self._richtig = richtig

        richtigeAntwort = self._antworten[richtig]
        random.shuffle(self._antworten)
        self._richtig = self._antworten.index(richtigeAntwort) + 1


    def __str__(self):
        return f"Your current level is {self._level}!\n{self._frage}\n(0) {self._antworten[0]}\n(1) {self._antworten[1]}\n(2) {self._antworten[2]}\n(3) {self._antworten[3]}\n"

     
def lineToQuestion(line):
    parts = line.split("\t")
    return Question(parts[0], parts[1], [parts[2], parts[3], parts[4], str(parts[5]).removesuffix("\n")], 0)

def getQuestions():
    datei = open("flask_millionaire/data/millionaire.txt", "r")
    datei.readline()
    lines = datei.readlines()
    questions = []
    for line in lines:
        questions.append(lineToQuestion(line))
    return questions

app = Flask(__name__)

level = 0
questions = getQuestions()
currentQuestion = Question(0, "", ["", "", ""], 0)


@app.route('/')
def home():
    global currentQuestion
    global level
    levelQuestions = []
    for question in questions:
                if int(question._level) == level:
                    levelQuestions.append(question)
    currentQuestion = levelQuestions[random.randint(0, (len(levelQuestions) - 1))]
    if level < 4:    
        return render_template('index.html', frage=currentQuestion._frage, antworten=currentQuestion._antworten)
    else:
        level = 0
        return render_template('finish.html', feedback="Du hast alle Fragen richtig beantwortet")

@app.route('/question')
@app.route('/question/<int:correct>')
def question(correct):
    global level
    global currentQuestion
    feedback = "Falsche Antwort. Die richtige Antwort wäre: " + str(currentQuestion._antworten[currentQuestion._richtig - 1])
    if correct == currentQuestion._richtig:
        feedback = "Richtige Antwort"
        level += 1
    else:
        level = 0
    return render_template('feedback.html', feedback=feedback, level=level)
    


if __name__ == '__main__':
    app.run(debug=True)