class ChatMemory:
    def __init__(self):
        self.history = []
        self.max_history = 10  # Limit history to last 10 messages

    def add(self, role, content):
        self.history.append({"role": role, "content": content})

        if len(self.history) > self.max_history * 2:
            self.history = self.history[-self.max_history * 2:]  # Remove oldest message to maintain limit

    def get(self):
        return self.history
    
    def clear(self):
        self.history = []