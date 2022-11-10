#jaruva name to change
# just a really useful voice assistant

import datetime
import traceback
from Automations.Logging import Logging, logMessage
# from Logging import Logging
import os
import subprocess
import webbrowser

import playsound
import speech_recognition
from gtts import gTTS

import mouse
from python_imagesearch.imagesearch import imagesearch

logging = Logging()

def Make_Directory(Path_Folder: str) -> str:
	"""
	Make a directory if it doesn't already exists
	Returns: A path to the folder
	"""
	if not os.path.exists(Path_Folder):
		os.makedirs(Path_Folder)

	return os.getcwd() + "/" + Path_Folder

def Speak(text: str) -> bool:
	"""
	Speak function take a string and converts it to an audio file and plays it.
	"""
	try:
		# Convert TextToAudio
		TextToSpeak = gTTS(text=text, lang="da")
		print(text)

		# Save the Audio to a file
		TextToSpeak.save("TTS" + text[:10] + ".mp3")

		# Play the the Audio file
		playsound.playsound("TTS" + text[:10] + ".mp3")

		# Remove the file
		os.remove("TTS" + text[:10] + ".mp3")
	except Exception as e:
		logging.log_message(logMessage(f"Exception in function 'Speak': {e}", "Automations.Funtions.py", "error", traceback.format_exc()))
		return False

	return True

def Get_Audio(language: str = "da-DK", timeout: int = 4) -> str:
	"""
	loops until recognition of audio to Text, language = "da-DK"
	"""
	said = ""
	Recognizer = speech_recognition.Recognizer()
	with speech_recognition.Microphone() as source:
		print("Lytter...")
		try:
			#Recognizer.adjust_for_ambient_noise(source, duration=0.5)
			audio = Recognizer.listen(source, timeout)
		except speech_recognition.WaitTimeoutError:
			return Get_Audio()
		print("Beregner...")

		try:
			said = Recognizer.recognize_google(audio, None, language=language)
			print(said)
		except Exception as e:
			print("Kunne ikke lytte", e)
			return Get_Audio()
			
		return said if said else Get_Audio()

def Get_clock(format = "%H:%M") -> str:
	"""
	Returns the current time with format\n
	Default format hours and minutes
	"""
	return datetime.datetime.now().strftime(format)

def Get_chromedir() -> str:
	return 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

def open_google(search: str = "", webside: str = "") -> bool:
	"""
	Open google and either search or vist webside.
	"""
	try:
		chromedir = Get_chromedir()
		if webside == "":
			webbrowser.get(chromedir).open(f"http://google.com/search?q={search}")
		else:
			webbrowser.get(chromedir).open(webside)
	except Exception as e:
		logging.log_message(logMessage(f"Exception in function 'open_google': {e}", "Automations.Funtions.py", "error", traceback.format_exc()))
		return False
	
	return True

def ingame() -> bool:
	"""
	Check if a game is open
	"""
	try:
		games = [b"League of Legends.exe", b"csgo.exe", b"Among Us.exe", b"BloonsTD6.exe", b"BrawlhallaGame.exe", b"Clicker Heroes.exe", b"factorio.exe", b"Golf With Your Friends.exe", b"GTA5.exe", b"Rust.exe", 
		b"Terraria.exe", b"tModLoader.exe", b"UNO.exe", b"FortniteClient-Win64-Shipping.exe", b"LoR.exe", b"VALORANT.exe", 
		]
		OpenPrograms = subprocess.check_output('tasklist', shell=True)
		
		for game in games:
			if game in OpenPrograms:
				return True
			
		return False
	except Exception as e:
		logging.log_message(logMessage(f"Exception in function 'ingame': {e}", "Automations.Funtions.py", "error", traceback.format_exc()))
		raise SystemError(e)

def open_program(program: str) -> bool:
	"""
	Start a program
	"""
	try:
		programs = {
			#.url (steam and epic games)
			"counter-strike global offensive": "C:\\Users\\theod\\OneDrive\\Skrivebord\\Counter-Strike Global Offensive.url",
			"clicker heroes": "C:\\Users\\theod\\OneDrive\\Skrivebord\\Clicker Heroes.url",
			"tModLoader": "C:\\Users\\theod\\OneDrive\\Skrivebord\\tModLoader.url",
			"terraria": "C:\\Users\\theod\\OneDrive\\Skrivebord\\Terraria.url",
			"factorio": "C:\\Users\\theod\\OneDrive\\Skrivebord\\Factorio.url",
			"fortnite": "C:\\Users\\theod\\OneDrive\\Skrivebord\\Terraria.url",
			"satisfactory early access": "C:\\Users\\theod\\OneDrive\\Skrivebord\\Satisfactory Early Access.url",
			#.lnk
			"league of legends": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\Programs\\League of Legends\\League of Legends.lnk"
		}
		os.startfile(programs[program])
		return True
	except Exception as e:
		logging.log_message(logMessage(f"Exception in function 'open_program': {e}", "Automations.Funtions.py", "error", traceback.format_exc()))
		return False


def FindImage(image: str, offset: tuple) -> list:
	postion = imagesearch(image, precision=0.75)
	if postion[0] == -1:
		logging.log_message(logMessage(f"Could not find image: {image}", "Automations.Funtions.py", "warning"))
		return None
	return [postion[0]+offset[0], postion[1]+offset[1]]

def MoveMouse(position: list) -> bool:
	if not isinstance(position, list):
		logging.log_message(logMessage(f"Position is not a list: {position}", "Automations.Funtions.py", "warning"))
		return False
	mouse.move(position[0], position[1])
	mouse.click()
	return True

if __name__ == "__main__":	
	FindImage("CsgoAccept.png", (2,2))
