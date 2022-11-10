from time import sleep

from Funtions import FindImage, MoveMouse

from Logging import Logging
from SetForeground import Set_Foregound


class AutomationCs(object):
    def __init__(self):
        self.logging = Logging()
        self.autoAccept = True
        self.offset = (125, 25)

    
    def set_cs_foreground(self) -> bool:
        if not Set_Foregound().set_foreground("Counter-Strike: Global Offensive - Direct3D 9"):
            self.logging.log_message("Counter-Strike: Global Offensive not found", "Automations.AutoCs.py", "warning")
            return False
        return True
    
    def cs_auto_accept(self) -> bool:
        while self.autoAccept:
            self.set_cs_foreground()
            PostionOfImage = FindImage("images/CsgoAccept.png", self.offset)
            if not PostionOfImage:
                sleep(1)
                continue
            MoveMouse(PostionOfImage)
            return True
        self.logging.log_message("Auto accept disabled", "Automations.AutoCs.py", "normal")
        return False

if __name__ == '__main__': 
    AutomationCs().cs_auto_accept()
