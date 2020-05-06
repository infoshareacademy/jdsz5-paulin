class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_warning(message):
    print(f"{bcolors.WARNING}{message}{bcolors.ENDC}")


def print_bold(message):
    print(f"{bcolors.BOLD}{message}{bcolors.ENDC}")


def print_info(message):
    print(f"{bcolors.OKBLUE}{message}{bcolors.ENDC}")


def print_accept(message):
    print(f"{bcolors.OKGREEN}{message}{bcolors.ENDC}")


def print_error(message):
    print(f"{bcolors.FAIL}{message}{bcolors.ENDC}")