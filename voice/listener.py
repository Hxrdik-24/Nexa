import speech_recognition as sr
import pyaudio


r = sr.Recognizer()

def listen():

    try:
        with sr.Microphone() as source:

            print("Listening now...")

            audio = r.listen(
                source,
                timeout=10,
                phrase_time_limit=10
            )

        print("Recognizing...")

        word = r.recognize_google(audio)

        print(f"[HEARD] {word}")

        return word.lower().strip()

    except sr.WaitTimeoutError:
        print("Listening timed out: No speech detected.")
        return None

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
        return None

    except sr.RequestError as e:
        print(f"Could not request results from Google service; {e}")
        return None

    except Exception as e:
        print(f"Error: {e}")
        return None