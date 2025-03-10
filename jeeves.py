#!/usr/bin/env python3
"""
Jeeves - Human-like browser typing automation
Main entry point for the application
"""

import argparse
import sys
import time
import json
from pathlib import Path
import colorama
from colorama import Fore, Style

from typing_core import Jeeves
from window_manager import list_browser_windows
from utils import print_banner

def create_default_config(file_path="typer_config.json"):
    """Create a default configuration file with comments."""
    config = Jeeves.DEFAULT_CONFIG
    
    try:
        with open(file_path, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"{Fore.GREEN}✓ Default configuration created at {Fore.CYAN}{file_path}{Style.RESET_ALL}")
        
        # Add comments to the file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Add header comment
        commented_content = (
            "// Jeeves Configuration File\n"
            "// This file controls typing behavior and window selection\n"
            "// You can edit this file directly or use the CLI to update it\n\n"
            + content
        )
        
        with open(file_path, 'w') as f:
            f.write(commented_content)
            
        return True
    except Exception as e:
        print(f"{Fore.RED}✗ Failed to create default configuration: {e}{Style.RESET_ALL}")
        return False

def main():
    """Main function to parse arguments and run the program."""
    # Initialize colorama
    colorama.init()
    
    # Parse arguments
    parser = argparse.ArgumentParser(
        description=f"{Fore.CYAN}Jeeves{Style.RESET_ALL} - Human-like browser typing automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Fore.YELLOW}Examples:{Style.RESET_ALL}
  {Fore.GREEN}Basic usage:{Style.RESET_ALL}
    python jeeves.py
  
  {Fore.GREEN}Type content from a specific file:{Style.RESET_ALL}
    python jeeves.py --file email.txt
  
  {Fore.GREEN}Type direct text:{Style.RESET_ALL}
    python jeeves.py --text "Hello, this is a test."
  
  {Fore.GREEN}List available windows:{Style.RESET_ALL}
    python jeeves.py --list-windows
  
  {Fore.GREEN}Create a default configuration file:{Style.RESET_ALL}
    python jeeves.py --create-config my_config.json
    
  {Fore.GREEN}Use a custom configuration:{Style.RESET_ALL}
    python jeeves.py --config my_config.json
  
  {Fore.GREEN}Modify typing speed:{Style.RESET_ALL}
    python jeeves.py --min-delay 0.02 --max-delay 0.1
  
{Fore.YELLOW}For more information, visit:{Style.RESET_ALL} https://github.com/niknal357/jeeves
"""
    )
    
    # Input options
    input_group = parser.add_argument_group(f"{Fore.CYAN}Input Options{Style.RESET_ALL}")
    input_group.add_argument("-f", "--file", type=str, help="Path to text file to type")
    input_group.add_argument("-t", "--text", type=str, help="Direct text to type")
    
    # Configuration options
    config_group = parser.add_argument_group(f"{Fore.CYAN}Configuration Options{Style.RESET_ALL}")
    config_group.add_argument("-c", "--config", type=str, help="Path to configuration file")
    config_group.add_argument("-s", "--save-config", type=str, help="Save current configuration to specified file")
    config_group.add_argument("--create-config", type=str, help="Create a default configuration file at the specified path")
    
    # Window options
    window_group = parser.add_argument_group(f"{Fore.CYAN}Window Options{Style.RESET_ALL}")
    window_group.add_argument("-w", "--window", type=str, help="Browser window title to target")
    window_group.add_argument("-i", "--window-index", type=int, help="Index of the window to use (if multiple match)")
    window_group.add_argument("--list-windows", action="store_true", help="List all visible windows and exit")
    
    # Typing behavior options
    typing_group = parser.add_argument_group(f"{Fore.CYAN}Typing Behavior Options{Style.RESET_ALL}")
    typing_group.add_argument("--min-delay", type=float, help="Minimum delay between keystrokes (seconds)")
    typing_group.add_argument("--max-delay", type=float, help="Maximum delay between keystrokes (seconds)")
    typing_group.add_argument("--mistake-rate", type=float, help="Probability of making typing mistakes (0.0-1.0)")
    
    # Other options
    other_group = parser.add_argument_group(f"{Fore.CYAN}Other Options{Style.RESET_ALL}")
    other_group.add_argument("-d", "--delay", type=int, default=3, help="Startup delay in seconds before typing begins")
    other_group.add_argument("-q", "--quiet", action="store_true", help="Quiet mode, minimal output")
    other_group.add_argument("-v", "--version", action="store_true", help="Show version information and exit")
    
    args = parser.parse_args()
    
    # Print banner unless quiet mode is enabled
    if not args.quiet:
        print_banner()
    
    # Show version and exit
    if args.version:
        import pyautogui
        print(f"{Fore.GREEN}Jeeves v1.0{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Python Version: {sys.version.split()[0]}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}PyAutoGUI Version: {pyautogui.__version__}{Style.RESET_ALL}")
        return
    
    # Create default config if requested
    if args.create_config:
        create_default_config(args.create_config)
        return
    
    # List windows if requested
    if args.list_windows:
        list_browser_windows()
        return
    
    # Initialize the typer with verbose mode based on quiet flag
    typer = Jeeves(args.config, verbose=not args.quiet)
    
    # Update config based on command line arguments
    if args.window:
        typer.config["browser"]["window_title"] = args.window
    
    if args.window_index is not None:
        typer.config["browser"]["window_index"] = args.window_index
    
    if args.min_delay is not None:
        typer.config["typing_speed"]["min_delay"] = args.min_delay
    
    if args.max_delay is not None:
        typer.config["typing_speed"]["max_delay"] = args.max_delay
    
    if args.mistake_rate is not None:
        typer.config["typing_speed"]["mistake_probability"] = args.mistake_rate
    
    # Save configuration if requested
    if args.save_config:
        typer.save_config(args.save_config)
        if args.save_config and not (args.file or args.text):
            return  # Exit if only saving config
    
    # Get text to type
    text_to_type = None
    if args.text:
        text_to_type = args.text
        if not args.quiet:
            print(f"{Fore.BLUE}ℹ Using provided text ({len(text_to_type)} characters){Style.RESET_ALL}")
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text_to_type = f.read()
            if not args.quiet:
                print(f"{Fore.BLUE}ℹ Loaded text from file: {Fore.CYAN}{args.file}{Fore.BLUE} ({len(text_to_type)} characters){Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}✗ Error reading file: {e}{Style.RESET_ALL}")
            return
    else:
        default_file = "text.txt"
        try:
            with open(default_file, 'r', encoding='utf-8') as f:
                text_to_type = f.read()
            if not args.quiet:
                print(f"{Fore.BLUE}ℹ Using text from default file: {Fore.CYAN}{default_file}{Fore.BLUE} ({len(text_to_type)} characters){Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"{Fore.RED}✗ No text provided and default file '{default_file}' not found.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}ℹ Use --file or --text to specify what to type.{Style.RESET_ALL}")
            return
    
    if not text_to_type:
        print(f"{Fore.RED}✗ No text to type. Exiting.{Style.RESET_ALL}")
        return
    
    # Countdown
    if not args.quiet:
        print(f"{Fore.YELLOW}⚠ Make sure the target window is ready to receive input!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}► Starting in {Fore.CYAN}{args.delay}{Fore.GREEN} seconds...{Style.RESET_ALL}")
        for i in range(args.delay, 0, -1):
            print(f"{Fore.CYAN}{i}...{Style.RESET_ALL}", end="\r", flush=True)
            time.sleep(1)
        print()  # New line after countdown
    
    # Type the text
    typer.type_with_realism(text_to_type)

if __name__ == "__main__":
    main()