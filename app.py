from flask import Flask, render_template, request, redirect, url_for, jsonify
from utils.timer import countdown
from quiz_engine.generator import generate_quiz

app = Flask(__name__)

# This will hold the current quiz data (just for simplicity here)
questions = []
score = 0
current_question = 0
name = ""
topic = ""
user_answers = {}

@app.route('/')
def index():
    # Display home page with a form to enter details
    return render_template('index.html')

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    global questions, score, current_question, name, topic, user_answers
    name = request.form['name']
    topic = request.form['topic']
    num_questions = int(request.form['num_questions'])

    # Generate quiz
    questions = generate_quiz(topic=topic, num_questions=num_questions)
    score = 0  # Reset score at the start
    current_question = 0
    user_answers = {}

    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    global current_question
    if current_question >= len(questions):
        return redirect(url_for('end_quiz'))
    q = questions[current_question]
    return render_template('quiz.html', question=q, question_id=current_question, name=name, topic=topic)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    global score, current_question, user_answers
    answer = request.form.get('answer', '').upper()
    question_id = int(request.form.get('question_id', -1))

    if question_id == current_question and answer:
        correct_answer = questions[question_id]['answer']
        user_answers[question_id] = answer
        if answer == correct_answer:
            score += 1
        current_question += 1
    else:
        # Invalid submission, ignore or handle as needed
        pass

    if current_question >= len(questions):
        return redirect(url_for('end_quiz'))
    else:
        return redirect(url_for('quiz'))

@app.route('/end_quiz')
def end_quiz():
    global score, user_answers
    return render_template('end_quiz.html', score=score, questions=questions, user_answers=user_answers)

@app.route('/reset_score', methods=['POST'])
def reset_score():
    global score
    score = 0
    return jsonify({'status': 'score reset'})

if __name__ == '__main__':
    app.run(debug=True)
