import json
import random
import re
import threading
from time import sleep

from Automations.Funtions import Get_Audio, Get_clock, Speak, open_program


class VoiceAssistant(object):
    
    def __init__(self) -> None:
        self.command: str = ""
        self.listening: bool = False
        self.keyword: str = "hej google " 
        self.keyword_active: bool = False
        self.threadCount: int = 5
        self.threads: list = []
        self.runing: bool = True
        self.ThreadOffset: float = 0.5

    def get_json(self) -> json:
        return json.loads(open("brain.json", "r").read())
    
    def listen_for_keyword(self) -> bool:
        while self.listening:
            self.command = Get_Audio().lower()
            if self.keyword in self.command:
                self.keyword_active = True
                self.command = self.command.replace(self.keyword, "")
                return True
        return False

    def start_listening_for_keywords(self):
        self.listening = True
        for i in range(self.threadCount):
            self.threads.append(threading.Thread(target=self.is_actionation_command))
            self.threads[i].start()
            sleep(self.ThreadOffset)
    
    def listen_for_command(self):
        if self.keyword_active:
            self.listening = False
            self.keyword_active = False

            if not self.execute_command():
                self.command = Get_Audio().lower()
                self.execute_command()
            
            self.start_listening_for_keywords()
    
    def execute_command(self) -> bool:
        print(self.command)
    
    def main(self):
        try:
            self.start_listening_for_keywords()
            while self.runing:
                self.listen_for_command()
        except KeyboardInterrupt:
            self.runing = False
            print("\nExiting...")

if __name__ == "__main__":
    VoiceAssistant().main()
