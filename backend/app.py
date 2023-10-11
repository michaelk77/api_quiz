import time
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:example@db/mydatabase'
db = SQLAlchemy(app)


class Question(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    question: str = db.Column(db.String(500))
    answer: str = db.Column(db.String(500))
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/', methods=['POST'])
def get_question() -> str:
    data: dict = request.get_json()
    questions_num: int = data.get('questions_num')
    last: str = get_last_question()

    questions: list = []
    while len(questions) < questions_num:
        response = requests.get(
            f'https://jservice.io/api/random?count={questions_num}')
        data = response.json()
        for item in data:
            if not Question.query.filter_by(
                    question=item['question']).first():
                questions.append(item)

    question_objs: list = []
    for question in questions:
        question_obj = Question(question=question['question'],
                                answer=question['answer'])
        db.session.add(question_obj)
        question_objs.append(question_obj)
    db.session.commit()
    return last


def get_last_question() -> str:
    question_obj: Question = Question.query.order_by(
        Question.created_at.desc()).first()
    if question_obj:
        return question_obj.question
    return ""


if __name__ == '__main__':
    with app.app_context():
        # Wait for the database to start
        time.sleep(1)
        db.create_all()
    app.run(host='0.0.0.0')
