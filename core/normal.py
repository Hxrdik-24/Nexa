from actions import informations , applications , browser
from brain.llm import apiprocess
from core.assistant import speak
class NormalMode:

    def open_chrome(self):
        applications.open_chrome()

    def open_youtube(self):
        applications.open_youtube()

    def take_screenshot(self):
        print("Taking screenshot")

    def open_vs_code(self):
        applications.open_vscode()

    def today_weather(self):
        informations.weathernow()

    def time_now(self):
        informations.timenow()

    def open_github(self):
        browser.openGithub()

    def open_lead_code(self):
        browser.openLeetcode()

    def open_insta(self):
        browser.openInsta()

    def open_facebook(self):
        browser.openFacebook()

    def default(self, command):
        api_response = apiprocess(command)
        speak(api_response)
