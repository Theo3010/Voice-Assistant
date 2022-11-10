import contextlib
from cmath import e, pi
import random
import traceback

from Automations.Funtions import Speak
from Automations.Logging import Logging, logMessage


class math(object):
    def __init__(self, logging: Logging = Logging()) -> None:
        self.WordToMathOperator = {
            "plus": "+",
            "minus": "-",
            "gange": "*",
            "multiplikation": "*",
            "x": "*",
            "divide": "/",
            "delt med": "/",
            "over": "/",
            "opløftet i": "**",
            "opløftet": "**",
            "komma": ".",
            ",": ".",
            "pi": str(pi),
        }
        self.respones = [
            "Svaret er Ans",
            "Ans",
            "Ans er Svaret",
            "Det giver Ans",
            "Det er lige med Ans"
        ]

        self.logging: Logging = logging

    def translate_TextToMath(self, command: str) -> str:
        """
        Tranaslate text to math.
        Eks: delt med = /

        TODO: Can't differentiate between e, as number, and e as letter.
        """
        splitCommand = command.split(" ")

        self.logging.log_message(logMessage(f"{splitCommand}", "Automations.math.py", "normal"))

        # Translate words to math operators
        for index, word in enumerate(splitCommand):
            
            # Check for to words math operators
            with contextlib.suppress(IndexError):
                ToWordMathOperator = f"{splitCommand[index]} {splitCommand[index + 1]}"
                if ToWordMathOperator in self.WordToMathOperator:
                    command = command.replace(ToWordMathOperator, self.WordToMathOperator[ToWordMathOperator])
            # Check for one word math operators
            if word in self.WordToMathOperator:
                command = command.replace(word, self.WordToMathOperator[word])


        self.logging.log_message(logMessage(f"{command}", "Automations.math.py", "normal"))
        return command
    
    def math(self, command: str) -> bool:
        # Translate text to math
        command = self.translate_TextToMath(command)
        
        try:
            # Evaluate math command
            result = round(eval(command),2)
            answer = (str(result).replace(".", ","))
            self.logging.log_message(logMessage(f"{command} = {answer}", "Automations.math.py", "normal"))

            # Picks a random response and replaces 'Ans' with the answer
            return Speak(random.choice(self.respones).replace("Ans", answer))
            
        except Exception as e:
            # Log error
            self.logging.log_message(logMessage(f"Exception in function 'math': {e}", "Automations.math.py", "error", traceback.format_exc()))
            return False


if __name__ == "__main__":
    math().math("2 delt med 3")
    