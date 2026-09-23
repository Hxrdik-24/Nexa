from voice.speaker import speak
import time 
import pyautogui as p

def open_chrome():
    speak("opening chrome ...")
    time.sleep(1)
    p.press('win')
    time.sleep(1)
    p.write('chrome',interval=0.3)
    p.press('enter')

def open_vscode():
    speak("Opening  visual studio code  ")
    time.sleep(1)
    p.press('win')
    time.sleep(1)
    p.write('vs code',interval=0.3)
    p.press('enter')

def open_youtube():
    speak("opening youtube ...")
    time.sleep(1)
    p.press('win')
    time.sleep(1)
    p.write('You tube',interval=0.3)
    p.press('enter')