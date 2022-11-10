import threading
from time import sleep, time

import keyboard

from Automations.Encryption import decrypt_password, read_from_json
from Automations.Funtions import FindImage, MoveMouse, Speak, open_program
from Automations.Logging import Logging, logMessage
from Automations.SetForeground import Set_Foregound


class AutomationLoL(object):
    def __init__(self, logging: Logging = Logging()) -> None:
        self.logging = logging
        self.usernames = {
            "eune": "theo1030",
            "eune2": "the03010",
            "euw": "UniloginMan",

        }
        self.regionName = {
            "eune": "EU Nord Øst",
            "eune2": "EU Nord Øst 2",
            "euw": "EU West",
        }
        self.autoAccept = True
        self.offset = (125, 25)

    def set_lol_Client_foreground(self) -> bool:
        if not Set_Foregound().set_foreground("Riot Client Main"):
            self.logging.log_message(logMessage(
                "League of Legends not found", "Automations.AutoLoL.py", "warning"))
            return False
        return True

    def set_lol_foreground(self) -> bool:
        if not Set_Foregound().set_foreground("League of Legends"):
            self.logging.log_message(logMessage(
                "League of Legends not found", "Automations.AutoLoL.py", "warning"))
            return False
        return True

    def open_lol(self) -> bool:
        if not open_program("league of legends"):
            self.logging.log_message(logMessage(
                "League of Legends not found", "Automations.AutoLoL.py", "warning"))
            return False
        return True

    def get_password(self, region: str) -> str:
        try:
            return decrypt_password(read_from_json()["lol"][region].encode("UTF_8"))
        except KeyError:
            self.logging.log_message(f"No password found for region: {region}", "Automations.AutoLoL.py", "warning")

            return ""

    def wait_for_program_to_start(self, timeout=5) -> bool:
        timeOutStart = time()
        while True:
            timeOutStop = time()
            if self.set_lol_Client_foreground():
                return True

            if timeOutStop - timeOutStart > timeout:
                self.logging.log_message(logMessage(
                    f"TimeOut: League of Legends did not start after {timeout} secounds", "Automations.AutoLoL.py", "warning"))
                return False

            sleep(.5)

    def login(self, region: str) -> bool:

        threading.Thread(target=Speak, args=(
            f"Okay, jeg vil nu logge ind i League of legends på {self.regionName[region]}",)).start()

        self.open_lol()

        if not self.wait_for_program_to_start():
            Speak("League of Legends startet ikke efter 5 sekunder")
            return False

        self.logging.log_message(logMessage(
            f"Logging in to League of Legends {self.regionName[region]}", "Automations.AutoLoL.py", "info"))

        if not self.set_lol_Client_foreground():
            Speak("League of Legends startet, men kunne ikke settes til forgrunden")
            return False

        sleep(.5)

        PostionOfUsernameLogin = FindImage(
            "images/lolLoginUsername.png", (0, 75))
        MoveMouse(PostionOfUsernameLogin)

        # sleep(.5)

        keyboard.write(self.usernames[region])
        keyboard.press_and_release("tab")

        keyboard.write(self.get_password(region))
        keyboard.press_and_release("enter")

        # sleep(.5)

        self.logging.log_message(logMessage(
            f"Logged in to League of Legends {self.regionName[region]}", "Automations.AutoLoL.py", "info"))

        return Speak(f"Nu er du logget ind på {region}")

    def lol_auto_accept(self, autoAccept: bool) -> bool:
        if isinstance(autoAccept, bool):
            self.autoAccept = autoAccept

        elif isinstance(autoAccept, str):
            self.autoAccept = autoAccept == "True"

        else:
            self.logging.log_message(
                logMessage(
                    message="autoAccept is not a boolean",
                    module="Automations.AutoLoL.py",
                    status="warning"
                )
            )
            raise TypeError("autoAccept must be a bool or a string")

        if not self.autoAccept:
            self.logging.log_message(
                logMessage(
                    message="AutoAccept is now disabled",
                    module="Automations.AutoLoL.py",
                    status="info")
            )
            return Speak("automatisk acceptere slået fra")

        while self.autoAccept:
            self.set_lol_foreground()
            PostionOfImage = FindImage("images/LolAccept.png", self.offset)
            if not PostionOfImage:
                sleep(1)
                continue
            MoveMouse(PostionOfImage)

            Speak("Accepteret")

        return True


if __name__ == '__main__':
    autolol = AutomationLoL()
    autolol.logging.PrintLog = False
    region = input("region: ")

    autolol.login(region)
    input("Press enter to continue")
