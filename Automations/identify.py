class Identify(object):

    def IdentifyKeyword(self, command: str, keywords: list) -> bool:
        if not isinstance(keywords, list):
            raise TypeError("keywords must be a list")

        if isinstance(keywords[0], list):
            for keywords in keywords:
                if all(keyword in command for keyword in keywords):
                    return True
            return False

        elif isinstance(keywords[0], str):
            for keyword in keywords:
                if keyword in command:
                    return True
            return False

        else:
            raise TypeError("keyword does not contain a string nor list")

    def IdentifyKewordArgs(self, command: str, args: list) -> str:
        for arg in args:
            if arg in command:
                return arg
        return ""


class IdentifyMath(object):

    def Identify(self, command: str) -> str:
        """
        Indentifies what of the command is math, if any.

        TODO: 
            -> Can't identify e was a number.\n
            -> Can mistake numbers in a none math command.
        """

        wordsInCommand = command.split(" ")
        for index, word in enumerate(wordsInCommand):
            if word.isdigit() or word in ["+", "-", "plus", "minus", "pi"]:
                mathStart = " ".join(wordsInCommand[index:])
                return mathStart
        return ""


if __name__ == '__main__':
    pass
