def ansi(color_id):
    return f"\u001b[{color_id}m"


reset = ansi(0)


def red(message):
    return f"{ansi(31)}{message}{reset}"


def green(message):
    return f"{ansi(32)}{message}{reset}"


def yellow(message):
    return f"{ansi(33)}{message}{reset}"


def blue(message):
    return f"{ansi(34)}{message}{reset}"


def magenta(message):
    return f"{ansi(35)}{message}{reset}"


def cyan(message):
    return f"{ansi(36)}{message}{reset}"


def red(message):
    return f"{ansi(37)}{message}{reset}"
