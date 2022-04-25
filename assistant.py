import re
import subprocess
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import time
import pyautogui

import pyttsx3

__name__ = "__main__"

voiceId = "ADD_YOUR_PATH\\TTS_MS_HU-HU_Szabolcs_11.0"
voiceIdEng ="ADD_YOUR_PATH\\TTS_MS_EN-US_DAVID_11.0"
powerpointPath = "ADD_YOUR_PATH"
excelPath = "ADD_YOUR_PATH"
wordPath = "ADD_YOUR_PATH"
chromePath = "ADD_YOUR_PATH"
musicPath = "ADD_YOUR_PATH"
paintPath = "ADD_YOUR_PATH"
notePath = "ADD_YOUR_PATH"
importantDaysPath = "ADD_YOUR_PATH"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voiceId)
engine.setProperty("rate", 158)

webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))


def importantDays():
    now = datetime.date.today()
    file = open(importantDaysPath, "r", encoding="utf8")
    text = file.read()
    text = re.split(',|\n', text)
    result = ""
    for index in range(0, len(text) - 3, 3):
        name = text[index]
        ageData = text[index + 1].split('.')
        nameData = text[index + 2].split('.')

        if (ageData[1] != '?' and ageData[2] != '?'):
            birthdayDateTime = "." + ageData[1] + "." + ageData[2]
            birtdayDate = datetime.datetime.strptime(str(now.year) + birthdayDateTime, '%Y.%m.%d').date()
            birtdayDays = str(now - birtdayDate)
            birtdayDays = birtdayDays.split(" ")

            if (birtdayDays[0] == "0:00:00"):
                if (ageData[0] != '?'):
                    age = str(now.year - int(ageData[0]))
                    result = result + name + " szülinapja ma van! " + age + " éves lett.\n"
                else:
                    result = result + name + " szülinapja ma van!\n"
            elif (int(birtdayDays[0]) > 0 and int(birtdayDays[0]) < 10):
                if (ageData[0] != '?'):
                    age = str(now.year - int(ageData[0]))
                    result = result + name + " " + age + " éves lett " + birtdayDays[0] + " napja!\n"
                else:
                    result = result + name + " szülinapja " + birtdayDays[0] + " napja volt!\n"
            elif (int(birtdayDays[0]) < 0 and int(birtdayDays[0]) > -15):
                if (ageData[0] != '?'):
                    age = str(now.year - int(ageData[0]))
                    result = result + name + " " + age + " éves lesz " + str(abs(int(birtdayDays[0]))) + " nap múlva!\n"
                else:
                    result = result + name + " szülinapja " +  str(abs(int(birtdayDays[0]))) + " nap múlva lesz!\n"

            if (nameData[0] != '?' and nameData[1] != '?'):
                namedayDateTime = "." + nameData[0] + "." + nameData[1]
                namedayDate = datetime.datetime.strptime(str(now.year) + namedayDateTime, '%Y.%m.%d').date()
                namedayDays = str(now - namedayDate)
                namedayDays = namedayDays.split(" ")

                if (namedayDays[0] == "0:00:00"):
                    result = result + name + " névnapja ma van!\n"
                elif (int(namedayDays[0]) > 0 and int(namedayDays[0]) < 10):
                    result = result + name + " névnapja " + namedayDays[0] + " napja volt!\n"
                elif (int(namedayDays[0]) < 0 and int(namedayDays[0]) > -25):
                    result = result + name + " névnapja " + str(abs(int(namedayDays[0]))) + " nap múlva lesz!\n"


    file.close()

    if( result == ""):
        return "Névnap és születésnap nem lesz mostanában!"
    return result


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Jó reggelt!")

    elif hour >= 12 and hour < 18:
        speak("Jó napot!")

    else:
        speak("Jó estét!")

    assname = ("Szergej 1 pont 0")
    speak("A virtuális aszisztensed vagyok")
    speak(assname)


def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Várom az utasítását...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Feldolgozás...")
        query = r.recognize_google(audio, language='hu-hu')
        print(f"Felhasználó parancsa: {query}\n")

    except Exception as e:
        print(e)
        print("Nem sikerült feldolgozni a hangját!")
        return ""

    return query


if __name__ == '__main__':
    clear = lambda: os.system('cls')

    clear()
    wishMe()

    while True:
        query = takeCommand().lower()

        if 'wikipédia' in query:
            wikipedia.set_lang("hu")
            speak('Wikipédián keresem...')
            query = query.replace("wikipédia", "")
            res = wikipedia.summary(query)
            res.split(".")
            results = ""

            if (len(res) >= 10):
                for r in range(len(res)):
                    results = results + res[r];
            else:
                for r in res:
                    results = results + r

            speak("A Wikipédia szerint")
            print(results)
            speak(results)

        elif 'nyisd meg a youtube' in query or 'youtube megnyitás' in query:
            speak("Parancs! Azonnal indítom!")
            webbrowser.get("chrome").open_new_tab('youtube.com')

        elif 'nyisd meg a google' in query or 'google megnyitás' in query:
            speak("Parancs! Azonnal indítom!")
            webbrowser.get("chrome").open_new_tab('google.hu')

        elif 'gmail' in query:
            speak("Azonnal indítom!")
            webbrowser.get("chrome").open_new_tab('mail.google.com/mail')

        elif 'zene indítás' in query or "indíts el egy zenét" in query:
            speak("Parancs! Azonnal indítom!")
            songs = os.listdir(musicPath)
            print(songs)
            random = os.startfile(os.path.join(musicPath, songs[1]))

        elif 'mennyi az idő' in query or 'hány óra van' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"A pontos idő {strTime}")
            speak(f"A pontos idő {strTime}")

        elif 'nyisd meg a böngészőt' in query or 'böngésző megnyitás' in query:
            codePath = r"ADD_YOUR_PATH\chrome.exe"
            os.startfile(codePath)

        elif 'zárd be magad' in query:
            speak("Rendben, megyek pihenni. Amennyiben szüksége van rám indítsa el a programot!")
            exit()

        elif 'mondj egy viccet' in query or 'mondj viccet' in query:
            speak("Parancs! Azonnal mondok egy viccet angolul.")
            engine.setProperty('voice', voiceIdEng)
            joke = pyjokes.get_joke(language='en', category='neutral')
            print(joke)
            speak(joke)
            engine.setProperty('voice', voiceId)


        elif 'excel' in query:
            speak("Parancs! Azonnal indítom az exelt!")
            os.startfile(excelPath)

        elif 'powerpoint' in query:
            speak("Parancs! Azonnal indítom a PowerPointot")
            os.startfile(paintPath)

        elif 'word' in query:
            speak("Parancs! Azonnal indítom a Wordöt!")
            os.startfile(wordPath)

        elif 'születésnap' in query or 'fontos napok' in query or 'névnap' in query:
            speak('Parancs! Azonnal nézem a fontos dátumokat!')
            res = importantDays()
            print(res)
            speak(res)

        elif 'számítógép kikapcsolás' in query:
            speak("Parancs! Azonnal kikapcsolom a számítógépét!")
            subprocess.call('shutdown /p /f')

        elif 'lomtár ürítés' in query or 'ürítsd ki a lomtárat' in query:
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
            speak("Parancs! A szemetest kiürítettem!")


        elif "hol található" in query or "keresd meg a térképen" in query or "térképen keresd" in query:
            query = query.replace("hol található", "")
            query = query.replace("keresd meg a térképen", "")
            query = query.replace("térképen keresd", "")
            location = query
            speak("Parancs! Azonnal keresem a térképen!")
            webbrowser.get("chrome").open_new_tab("https://www.google.hu/maps/place/" + location + "")

        elif "índísd újra a számítógépet" in query or 'számítógép újraindítás' in query:
            subprocess.call(["shutdown", "/r"])

        elif "jegyzettömbe írd" in query or 'írd jegyzettömb' in query or 'jegyzetel' in query:
            speak("Mit írjak le?")
            note = takeCommand()

            file = open(notePath, "r", encoding="utf8")
            text = file.read()
            file.close()

            file = open(notePath, 'w')
            speak("Akar majd még hozzá írni?")
            command = takeCommand()
            if 'nem' in command:
                timeDate = str(datetime.date.today())
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write("\n*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")
                file.write(timeDate + " ")
                file.write(strTime + "\n")
                file.write(note)
                file.write(text)
            else:
                file.write(note)
                file.write(text)

            file.close()
            speak("Jegyzet írás befejeződött!")

        elif "jegyzet megnyitás" in query or 'nyisd meg a jegyzetet' in query:
            speak("Parancs! Azonnal menyitom a jegyzeteket!")
            file = open(notePath, "r")
            print(file.read())

        elif "szergej" in query:
            wishMe()
            speak("Várom az utasításod")

        elif "időjárás" in query:
            speak("Parancs! Időjárási információk keresése!")
            location = query
            webbrowser.get("chrome").open_new_tab("google.hu/search?q=időjárás")

        elif "facebook" in query:
            speak("Parancs! Facebook indítása!")
            location = query
            webbrowser.get("chrome").open_new_tab("facebook.com")

        elif 'hírek' in query:
            speak("Parancs! Hírek keresése folyamatban!")
            webbrowser.get("chrome").open_new_tab("google.com/search?q=" + query)

        elif 'keresés' in query or 'keresd meg' in query:
            query = query.replace("keresd meg", "")
            query = query.replace("keresés", "")
            webbrowser.get("chrome").open_new_tab("hirstart.hu")


        elif 'előző lap' in query or 'előző oldal' in query:
            speak("Parancs! Előző oldalra viszem a böngészőt!")
            pyautogui.keyDown('alt')
            pyautogui.press('left')
            pyautogui.keyUp('alt')

        elif 'következő lap' in query or 'következő oldal' in query:
            speak("Parancs! A következő oldalra viszem a böngészőt!")
            pyautogui.keyDown('alt')
            pyautogui.press('right')
            pyautogui.keyUp('alt')

        elif 'lap bezárás' in query or 'oldal bezárás' in query:
            speak("Parancs! Lap bezárása folyamatban!")
            pyautogui.keyDown('ctrl')
            pyautogui.press('w')
            pyautogui.keyUp('ctrl')

