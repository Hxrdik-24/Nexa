from voice.listener import listen
from voice.speaker import speak
from core.normal import NormalMode
from core.agent import NexaAgentic
from core.engNormal import EnglearnMode
class NexaAssistant:
    def __init__(self):
        self.current_mode = 1
        self.modeName = "Normal 🟢"

        print(f"[INIT] Nexa Assistant initialized in Mode {self.modeName}")

    def getModeobj(self,modeNum):
        if modeNum == 1:
            normal = NormalMode()
            return normal
        elif modeNum == 3:
            agentic = NexaAgentic()
            return agentic
        elif modeNum == 2:
            englearn =  EnglearnMode()
            return englearn
        else:
            pass
        
    def switchMode(self):
        speak("Please tell the mode name ")
        command = listen()
        command = command.lower()

        if "switch to mode 1" in command or "normal mode" in command:
            self.current_mode = 1
            self.modeName = "Normal 🟢"
            speak("Switched to Normal Assistant Mode.")

        elif "switch to mode 2" in command or "english learning" in command:
            self.current_mode = 2
            self.modeName = "English Learning Mode 🔵"
            speak("Switched to English Learning Mode.")

        elif "switch to mode 3" in command or "agentic mode" in command:
            self.current_mode = 3
            self.modeName = "Agentic Mode 🔴"
            speak("Switched to Agentic Mode.")

        else:
            print('please tell the mode name ')
            return False

        print("|-------------------------------------|")
        print(f"| Current Mode  |    {self.modeName}  |")
        print("|-------------------------------------|")

        return True

    def run(self):
        speak("Powering up System ...")
        print("to change the mode speak 'change mode' ")
        while True:
            command = listen()


            if not command:
                continue
            if "change mode" in command.lower():
                self.switchMode()      
                continue  
            command = command.replace(" ", "_")
            mode = self.getModeobj(self.current_mode)


            function = getattr(
                mode,
                command,
                None
            )
            if function:
                function()
            else:
                mode.default(command)