import uuid

class QuizRoom:
    def __init__(self, topic, num_questions):
        self.room_id = str(uuid.uuid4())[:6].upper()
        self.topic = topic
        self.num_questions = num_questions
        self.players = {}
        self.questions = []  # Fill after generation

    def add_player(self, name):
        if name not in self.players:
            self.players[name] = {
                "score": 0,
                "answers": []
            }

    def record_answer(self, name, q_idx, is_correct):
        if name in self.players:
            if is_correct:
                self.players[name]["score"] += 1
            self.players[name]["answers"].append((q_idx, is_correct))

    def get_scores(self):
        return {name: p["score"] for name, p in self.players.items()}
