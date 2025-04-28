from utils.timer import countdown

def start_quiz_ui(questions, time_per_question=15):
    score = 0
    for idx, q in enumerate(questions):
        print(f"\nQ{idx+1}: {q['question']}")
        for opt, val in q["options"].items():
            print(f"  {opt}) {val}")

        print(f"\nYou have {time_per_question} seconds to answer:")
        countdown(time_per_question)

        ans = input("Your answer (A/B/C/D): ").strip().upper()
        if ans == q["answer"]:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Incorrect! Correct answer was {q['answer']}")
    
    print(f"\n🎉 Quiz Over! Your Score: {score}/{len(questions)}")
