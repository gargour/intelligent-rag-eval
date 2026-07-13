class ConversationMemory:
    """Mémoire simple en mémoire vive (pour session Streamlit)."""
    def __init__(self, max_turns: int = 10):
        self.history: list[dict] = []
        self.max_turns = max_turns

    def add_turn(self, question: str, answer: str):
        self.history.append({"question": question, "answer": answer})
        if len(self.history) > self.max_turns:
            self.history.pop(0)

    def get_context_string(self) -> str:
        return "\n".join(
            f"Q: {h['question']}\nR: {h['answer']}" for h in self.history
        )