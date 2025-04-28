# main.py
from quiz_engine.generator import generate_quiz
from ui.widgets import start_quiz_ui
from quiz_engine.quiz_room import QuizRoom
from utils.timer import countdown

def main():
    print("🤖 Welcome to AI_FLASHMIND_2025!")

    name = input("Enter your name: ").strip()
    topic = input("Enter a quiz topic (e.g., Python, History, AI): ").strip()
    num_questions = input("How many questions? (default 5): ").strip()
    num_questions = int(num_questions) if num_questions.isdigit() else 5

    room = QuizRoom(topic=topic, num_questions=num_questions)
    room.add_player(name)

    print("\n📡 Generating quiz... Please wait.\n")
    questions = generate_quiz(topic=room.topic, num_questions=room.num_questions)
    room.questions = questions

    score = 0
    for q in questions:
        print(f"{q['question']}")
        countdown(15, print)  # Pass print as display_func
        try:
            answer = input("Your answer (A/B/C/D): ").strip().upper()
        except EOFError:
            print("\nInput ended unexpectedly. Exiting quiz.")
            break

        if answer == q['answer']:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Incorrect! Correct answer was {q['answer']}")

    print(f"\n🎉 Quiz Over! Your final score: {score}/{num_questions}")
    print(f"🏁 {name}'s final score: {score}/{num_questions}")

if __name__ == "__main__":
    main()
