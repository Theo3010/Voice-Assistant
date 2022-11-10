import json
import threading
import traceback

from Automations.AutoLoL import AutomationLoL
from Automations.Logging import Logging, logMessage


from Automations.Funtions import Get_Audio, Speak
from Automations.math import math
from Automations.identify import Identify, IdentifyMath

# "Lexis": "logical executive intelligence system"


class VoiceAssistant(object):

    def __init__(self) -> None:
        # Name of the voice assistant
        self.keywords = ["lexis", "lexus", "alex", "google"]
        self.listening = True

        self.logging: Logging = Logging()
        self.logging.PrintLog = True
        self.logging.PrintTraceback = True

        # Modules
        self.AutomationLoL: AutomationLoL = AutomationLoL(self.logging)

    def Wait_for_keyword(self) -> bool:
        while self.listening:
            command = Get_Audio().lower()
            for keyword in self.keywords:
                if keyword in command:
                    threading.Thread(
                        target=self.Process_command,
                        args=((command.replace(f"{keyword} ", "")),),
                        daemon=True
                    ).start()
                    break
        return True

    def Process_command(self, rawcommand: str) -> bool:
        try:
            # get json from file
            commands: list = json.load(open("commands.json"))

            # loop through commands
            for command in commands:

                # check if voice command is a valid command
                if Identify().IdentifyKeyword(rawcommand, command["keyword"]):
                    if not command["args"]:
                        # return result of command when called
                        return eval(f"{command['function']}()")

                    # get arguments from voice command
                    rawargument = Identify().IdentifyKewordArgs(
                        rawcommand, command["args"])

                        # convert voice arguments to vaild arguments
                    argument = command["argsToCommand"][rawargument or command["defualtArgs"]]

                    # return reslut of command when called
                    print(f"{command['function']}('{argument}')")
                    return eval(f"{command['function']}('{argument}')")
            if command := IdentifyMath().Identify(rawcommand):
                return math().math(command)

            self.logging.log_message(
                logMessage(
                    message=f"Command not found {rawcommand}",
                    module="VoiceAssistant.py",
                    status="warning"
                )
            )
            Speak("Det forstod jeg ikke")

        except Exception as e:
            self.logging.log_message(logMessage(message=f"Exception in function 'Process_command': {e}", module="VoiceAssistant.py", status="error", traceback=traceback.format_exc()))

            Speak("Der skete en fejl, prøv igen eller kontakt support")

    def main(self) -> bool:
        self.logging.log_message(
            logMessage(
                message="VoiceAssistant started",
                module="VoiceAssistant.py",
                status="info"
            )
        )

        # Start the voice assistant
        while self.listening:
            self.Wait_for_keyword()

        # Write the log to file
        with open("log.txt", "w") as f:
            f.write(self.logging.get_log())

        self.logging.log_message(
            logMessage(
                message="VoiceAssistant stopped",
                module="VoiceAssistant.py",
                status="info"
            )
        )
        return True


if __name__ == "__main__":
    print(VoiceAssistant().main())
    # print(VoiceAssistant().Process_command("hej lexis, 2 + 2"))
