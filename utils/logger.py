from colorama import Fore, init
from utils.config import DEBUG

TYPE_DEBUG = "DEBUG"
TYPE_INFO = "INFO"
TYPE_WARNING = "WARNING"
TYPE_ERROR = "ERROR"

init(autoreset=True)

def log_debug(message: str):
    if DEBUG: _print_log_message(message, Fore.YELLOW + TYPE_DEBUG)

def log_info(message: str):
    _print_log_message(message, Fore.CYAN + TYPE_INFO)

def log_warning(message: str):
    _print_log_message(message, Fore.MAGENTA + TYPE_WARNING)

def log_error(message: str):
    _print_log_message(message, Fore.LIGHTRED_EX + TYPE_ERROR)

def _print_log_message(message: str, type: str):
    print(type + ": " + Fore.WHITE + message)
