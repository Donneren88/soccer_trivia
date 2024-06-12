from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Question, Score, User
from app import db
import random

main = Blueprint('main', __name__)
trivia = Blueprint('trivia', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        avatar = request.form['avatar']
        current_user.avatar = avatar
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile'))
    return render_template('profile.html')

@main.route('/leaderboard')
def leaderboard():
    scores = Score.query.order_by(Score.score.desc()).limit(10).all()
    return render_template('leaderboard.html', scores=scores)

@trivia.route('/play')
@login_required
def play():
    session['score'] = 0
    session['question_index'] = 0
    return render_template('play.html')

@trivia.route('/get_question')
@login_required
def get_question():
    question_index = session.get('question_index', 0)
    questions = Question.query.all()
    if question_index >= len(questions):
        save_score()
        return jsonify({'end': True, 'score': session['score']})
    
    question = questions[question_index]
    session['question_index'] += 1
    return jsonify({
        'id': question.id,
        'question_text': question.question_text,
        'options': [question.option1, question.option2, question.option3, question.option4]
    })

@trivia.route('/submit_answer', methods=['POST'])
@login_required
def submit_answer():
    data = request.json
    question = Question.query.get(data['question_id'])
    if question and question.correct_option == data['answer']:
        session['score'] += 1
    return jsonify({'score': session['score']})

def save_score():
    score = Score(user_id=current_user.id, score=session['score'])
    db.session.add(score)
    db.session.commit()
