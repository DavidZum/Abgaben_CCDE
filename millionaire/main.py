import random

class Question:
    
    def __init__(self, level, frage, antworten, richtig):
        self._level = level
        self._frage = frage
        self._antworten = antworten
        self._richtig = richtig
        richtigeAntwort = self._antworten[richtig]
        random.shuffle(self._antworten)
        i = 0
        for antwort in self._antworten:
            if antwort == richtigeAntwort:
                self._richtig = i
            i += 1

    def __str__(self):
        return f"Your current level is {self._level}!\n{self._frage}\n(0) {self._antworten[0]}\n(1) {self._antworten[1]}\n(2) {self._antworten[2]}\n(3) {self._antworten[3]}\n"
        
    
def lineToQuestion(line):
    parts = line.split("\t")
    return Question(parts[0], parts[1], [parts[2], parts[3], parts[4], str(parts[5]).removesuffix("\n")], 0)

def getQuestions():
    datei = open("Aufgabe05/millionaire.txt", "r")
    datei.readline()
    lines = datei.readlines()
    questions = []
    for line in lines:
        questions.append(lineToQuestion(line))
    return questions
    

if __name__=='__main__':
    level = 0
    questions = getQuestions()
    levelQuestions = []
    antwort = 0
    if(antwort == 0):
        while level < 5:
            for question in questions:
                if int(question._level) == level:
                    levelQuestions.append(question)
            question = levelQuestions[random.randint(0, (len(levelQuestions) - 1))]
            print(question)
            antwort = int(input("Antwort: "))
            if antwort == question._richtig:
                level += 1
                print("Richtige Antwort!\n")
            else:
                level = 0
                print(f"Falsche Antwort! Die richtige Antwort wäre: {question._antworten[question._richtig]}\n")
            levelQuestions = []
        print("Du hast alles richtig beantwortet\n Möchtest du nocheinmal spielen? Ja(0) Nein(1)")
        antwort = int(input("Antwort: "))