from datetime import datetime
from dataclasses import dataclass
import traceback

@dataclass
class logMessage:
    message: str
    module: str
    status: str = "normal"
    traceback: traceback = None

class Logging(object):
    def __init__(self):
        self.PrintLog = True
        self.PrintTraceback = True
        self.log = ""
        self.color = {
            "error": "\033[1;31;40m",
            "warning": "\033[1;33;40m",
            "normal": "\033[0m",
            "info": "\033[0m"
        }
    
    def log_message(self, message: logMessage) -> None:
        message = self.format(message)
        self.log += message + "\n"
        
        if self.PrintLog:
            print(message)
    
    def get_log(self) -> str:
        return self.log
    
    def format(self, message: logMessage) -> str:
        return f"{self.color[message.status]}[{datetime.now().strftime('%H:%M:%S')} -- {message.module}] {message.message} {self.color['normal']}\n{message.traceback}" if message.traceback and self.PrintTraceback else f"{self.color[message.status]}[{datetime.now().strftime('%H:%M:%S')} -- {message.module}] {message.message} {self.color['normal']}"

if __name__ == "__main__":
    try:
        a = 100 / 0
    except Exception as e:
        Logging().log_message(logMessage("Dette er en test", "Logging.py", "warning", traceback.format_exc()))