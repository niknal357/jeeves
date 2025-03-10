from colorama import Fore, Style
import colorama

def print_banner():
    """Print a nice banner for the application."""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════╗
║ {Fore.YELLOW}Jeeves {Fore.GREEN}v1.0                                          {Fore.CYAN}║
║ {Fore.WHITE}Realistic browser typing automation                  {Fore.CYAN}║
╚══════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)