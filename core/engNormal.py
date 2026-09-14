from core.normal import NormalMode
from voice.speaker import speak
class EnglearnMode(NormalMode):
    def __int__(self):
        speak("speak start English learning  ")

    def start_english_learning(self):
        print("Wellcome to Nexa English Learning Mode ")
        print("-----------------------------------------------")
        
        

    def default(self, command):
        print(f"English Mode Don't Understand :- {command} ")
        return super().default(command)
