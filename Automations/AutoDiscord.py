from time import sleep

import keyboard

from Logging import Logging
from SetForeground import Set_Foregound
from Funtions import FindImage, MoveMouse


class AutomationDiscord(object):
    def __init__(self):
        self.logging = Logging()
        self.offset = (25, 15)

    # Set the foreground to the Discord window
    def set_discord_foreground(self):
        if not Set_Foregound().set_foreground("(Discord|.+? - Discord)"):
            self.logging.log_message("Discord not found", "Automations.AutoDiscord.py", "error")
            return False
        return True

    
    # Switch Discord channel
    def SwitchChannel(self, channel: str) -> bool:
        if not self.set_discord_foreground():
            return False
        sleep(0.005)
        keyboard.press_and_release("ctrl+k")
        sleep(0.005)
        keyboard.write(channel)
        sleep(0.08)
        keyboard.press_and_release("enter")
        return True
    
    def answer_call(self):
        self.set_discord_foreground()
        PostionOfImage = FindImage("images/DiscordPickUpCall.png", self.offset)
        if not PostionOfImage:
            self.logging.log_message("Image found, postion null", "Automations.AutoDiscord.py", "error")
            return False
        MoveMouse(PostionOfImage)
    
    def recejct_call(self):
        self.set_discord_foreground()
        PostionOfImage = FindImage("images/DiscordRejectCall.png", self.offset)
        if not PostionOfImage:
            self.logging.log_message("Image found, postion null", "Automations.AutoDiscord.py", "error")
            return False
        MoveMouse(PostionOfImage)

    def end_call(self):
        self.set_discord_foreground()
        PostionOfImage = FindImage("images/DiscordEndCall.png", self.offset)
        if not PostionOfImage:
            self.logging.log_message("Image found, postion null", "Automations.AutoDiscord.py", "error")
            return False
        MoveMouse(PostionOfImage)
    
    def call(self, UserName: str):
        self.SwitchChannel(UserName)
        sleep(0.05)

        if PostionOfImage := FindImage("images/DiscordCall.png", self.offset):
            MoveMouse(PostionOfImage)
            return True

        sleep(0.05)

        if PostionOfImage := FindImage("images/DiscordCall.png", self.offset):
            MoveMouse(PostionOfImage)
            return True

        self.logging.log_message("Image found, postion null", "Automations.AutoDiscord.py", "error")
        return False
    
    def switch_VoiceActivityDetection(self):
        self.set_discord_foreground()
        keyboard.press_and_release("shift+ctrl+p")

    def switch_screen_share(self):
        self.set_discord_foreground()
        keyboard.press_and_release("shift+ctrl+s")

if __name__ == '__main__':
    Adiscord = AutomationDiscord()
    Adiscord.logging.set_logging(True)
    Adiscord.switch_VoiceActivityDetection()
