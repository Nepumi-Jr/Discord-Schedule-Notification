import sys


class colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\x1b[0m"
    # ? From OTOG


def printAny(head: str, content: str, color: str, alt: str):
    if sys.platform == "linux" or sys.platform == "linux2":
        print(f"[{color}{head}{colors.RESET}]{content}")
    else:
        print(f"{alt}[{head}]{content}")


def printWarning(head: str, content: str):
    printAny(head, content, colors.WARNING, "/!\\")


def printError(head: str, content: str):
    printAny(head, content, colors.FAIL, "(X)")


def printSuggest(head: str, content: str):
    printAny(head, content, colors.OKBLUE, "<.>")
