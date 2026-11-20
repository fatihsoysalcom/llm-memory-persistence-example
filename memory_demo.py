import json

class SimpleMemory:
    def __init__(self, filename="memory.json"):
        self.filename = filename
        self.memory = self.load_memory()

    def load_memory(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return [] # Start with an empty memory if file doesn't exist

    def save_memory(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=4)

    def add_to_memory(self, entry):
        self.memory.append(entry)
        self.save_memory()

    def get_recent_memory(self, limit=5):
        # Return the most recent entries, simulating a short-term context window
        return self.memory[-limit:]

    def get_full_memory(self):
        # For demonstration, we can also retrieve everything
        return self.memory

class ForgetfulAgent:
    def __init__(self, name="Agent"):
        self.name = name
        self.memory = SimpleMemory()

    def interact(self, user_input):
        # Simulate agent's thought process: check memory, then respond
        print(f"\n{self.name} received: '{user_input}'")

        # --- Memory Persistence Mechanism --- 
        # Before responding, add the current interaction to memory
        self.memory.add_to_memory({"role": "user", "content": user_input})

        # Get recent conversation history to inform the response
        recent_context = self.memory.get_recent_memory(limit=3) # Use last 3 turns as context
        print(f"{self.name} considering context: {recent_context}")

        # --- Response Generation (Simplified) ---
        if "merhaba" in user_input.lower():
            response = "Merhaba! Size nasıl yardımcı olabilirim?"
        elif "adın ne" in user_input.lower():
            response = f"Ben {self.name}."
        elif "unutkanlık" in user_input.lower():
            response = "Evet, ajanların unutkanlığı önemli bir sorun. Bellek mekanizmalarıyla bunu çözebiliriz."
        elif "ne konuştuk" in user_input.lower():
            if len(recent_context) > 1: # Check if there's prior conversation
                last_user_message = recent_context[-2]['content'] if len(recent_context) > 1 else "önceki bir şey"
                response = f"En son sizinle '{last_user_message}' hakkında konuşuyorduk gibi hatırlıyorum."
            else:
                response = "Henüz pek bir şey konuşmadık."
        else:
            response = "Anladım."

        # Add agent's response to memory as well
        self.memory.add_to_memory({"role": "agent", "content": response})
        self.memory.save_memory() # Ensure memory is saved after each turn

        return response

if __name__ == "__main__":
    agent = ForgetfulAgent("Akıllı Ajan")

    print("--- Ajanla Sohbet Başlıyor (Bellek Aktif) ---")
    print("Bellek 'memory.json' dosyasına kaydedilecektir.")

    while True:
        user_input = input("Siz: ")
        if user_input.lower() == "çıkış":
            print("Sohbet sona erdi.")
            break
        agent_response = agent.interact(user_input)
        print(f"{agent.name}: {agent_response}")

    print("\n--- Bellek İçeriği (memory.json) --- ")
    try:
        with open("memory.json", 'r', encoding='utf-8') as f:
            print(f.read())
    except FileNotFoundError:
        print("Bellek dosyası oluşturulmadı.")
