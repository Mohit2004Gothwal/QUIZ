import google.generativeai as genai
import os
import re
from dotenv import load_dotenv

load_dotenv()  # to load your API key from .env

# Set up your Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_quiz(topic, num_questions=5):
    prompt = f"Generate {num_questions} multiple choice questions on the topic '{topic}' with 4 options (A-D) and clearly mention the correct answer."

    model = genai.GenerativeModel('models/gemini-1.5-pro')

    response = model.generate_content(prompt)

    print("DEBUG: Gemini API response:")
    print(response.text)

    questions = parse_quiz_response(response.text)

    if not questions:
        print("ERROR: No questions parsed from Gemini response.")
        raise ValueError("Failed to generate quiz questions properly. Please try again.")

    return questions


def parse_quiz_response(response_text):
    """
    Parses the Gemini response and returns a list of questions with options and answers.
    Uses regex to extract question blocks.
    """
    question_pattern = re.compile(
        r'\*\*\d+\.\s*(.*?)\*\*Correct Answer:\*\*\s*\((.)\)\s*(.*?)\n\n',
        re.DOTALL
    )
    option_pattern = re.compile(r'\((A|B|C|D)\)\s*(.*)')

    questions = []

    # Split response into question blocks by looking for question numbers
    blocks = re.split(r'\n\s*\*\*\d+\.', response_text)
    for block in blocks:
        if not block.strip():
            continue

        # Extract question text (up to first option)
        question_match = re.match(r'(.*?)\n', block, re.DOTALL)
        if not question_match:
            continue
        question_text = question_match.group(1).strip()

        # Extract options
        options = {}
        for opt_match in option_pattern.finditer(block):
            key = opt_match.group(1)
            val = opt_match.group(2).strip()
            options[key] = val

        # Extract answer
        answer_match = re.search(r'\*\*Correct Answer:\*\*\s*\((.)\)', block)
        answer = answer_match.group(1) if answer_match else ""

        if question_text and options and answer:
            questions.append({
                "question": question_text,
                "options": options,
                "answer": answer
            })

    return questions

def fallback_sample_questions(num_questions):
    return [
        {
            "question": f"What is the output of print(2 ** {i})?",
            "options": {
                "A": str(2 ** i),
                "B": str(i * 2),
                "C": str(i + 2),
                "D": "Syntax Error"
            },
            "answer": "A"
        } for i in range(1, num_questions + 1)
    ]

