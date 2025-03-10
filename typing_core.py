"""
Jeeves - Human-like browser typing automation
Core typing functionality and config management
"""

import json
import os
import random
import time
import pyautogui
from tqdm import tqdm
import colorama
from colorama import Fore, Style

from window_manager import find_browser_window
from keyboard_layout import get_nearby_keys


class Jeeves:
    """A class to handle realistic typing automation in browser windows."""
    
    DEFAULT_CONFIG = {
        "typing_speed": {
            "min_delay": 0.05,  # Minimum delay between keystrokes (seconds)
            "max_delay": 0.15,  # Maximum delay between keystrokes (seconds)
            "mistake_probability": 0.03,  # Probability of making a typo
            "correction_delay": 0.5,  # Delay before correcting a typo (seconds)
        },
        "human_behavior": {
            "pause_probability": 0.1,  # Probability of taking a pause while typing
            "min_pause_duration": 0.5,  # Minimum pause duration (seconds)
            "max_pause_duration": 2.0,  # Maximum pause duration (seconds)
            "paragraph_pause": 1.0,  # Pause after typing a paragraph (seconds)
        },
        "browser": {
            "window_title": "Chrome",  # Window title to search for
            "focus_delay": 1.0,  # Delay after focusing the window (seconds)
            "window_index": 0,  # Which window to use if multiple are found (0 = first)
        }
    }
    
    def __init__(self, config_path=None, verbose=True):
        """Initialize the Jeeves with configuration."""
        # Initialize colorama for cross-platform colored terminal output
        colorama.init()
        
        # Initialize state
        self.current_browser_window = None
        self.verbose = verbose
        
        # Load configuration
        self.config = self.load_config(config_path)
    
    def load_config(self, config_path):
        """Load configuration from a JSON file or use defaults."""
        config = self.DEFAULT_CONFIG.copy()
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                
                # Update configuration with user settings
                for category in user_config:
                    if category in config:
                        config[category].update(user_config[category])
                
                if self.verbose:
                    print(f"{Fore.GREEN}✓ Configuration loaded from {Fore.CYAN}{config_path}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}✗ Error loading configuration: {e}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}ℹ Using default configuration{Style.RESET_ALL}")
        else:
            if self.verbose:
                if config_path:
                    print(f"{Fore.YELLOW}ℹ Config file {Fore.CYAN}{config_path}{Fore.YELLOW} not found{Style.RESET_ALL}")
                print(f"{Fore.BLUE}ℹ Using default configuration{Style.RESET_ALL}")
        
        return config
    
    def save_config(self, config_path="typer_config.json"):
        """Save the current configuration to a JSON file."""
        try:
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            if self.verbose:
                print(f"{Fore.GREEN}✓ Configuration saved to {Fore.CYAN}{config_path}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}✗ Error saving configuration: {e}{Style.RESET_ALL}")
            return False
    
    def type_with_realism(self, text):
        """Type text with realistic human-like behavior."""
        if not self.current_browser_window:
            window_title = self.config["browser"]["window_title"]
            window_index = self.config["browser"]["window_index"]
            self.current_browser_window = find_browser_window(window_title, window_index, self.verbose)
            if not self.current_browser_window:
                return False
            
            # Focus delay
            time.sleep(self.config["browser"]["focus_delay"])
        
        total_chars = len(text)
        if self.verbose:
            print(f"{Fore.GREEN}► Starting to type {Fore.CYAN}{total_chars}{Fore.GREEN} characters...{Style.RESET_ALL}")
        
        # Create progress bar
        with tqdm(total=total_chars, 
                  desc="Typing progress", 
                  unit="chars",
                  bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
                  disable=not self.verbose) as pbar:
            
            # Process text character by character
            i = 0
            typos = 0
            pauses = 0
            
            while i < total_chars:
                # Simulate a pause in typing (thinking or distraction)
                if random.random() < self.config["human_behavior"]["pause_probability"]:
                    pause_duration = random.uniform(
                        self.config["human_behavior"]["min_pause_duration"],
                        self.config["human_behavior"]["max_pause_duration"]
                    )
                    time.sleep(pause_duration)
                    pauses += 1
                
                # Paragraph pause (if we hit a newline character)
                if i > 0 and text[i-1] == '\n' and text[i] == '\n':
                    time.sleep(self.config["human_behavior"]["paragraph_pause"])
                
                # Type the current character
                current_char = text[i]
                
                # Simulate making a typo
                if random.random() < self.config["typing_speed"]["mistake_probability"]:
                    # Make a mistake (press a nearby key)
                    nearby_keys = get_nearby_keys(current_char)
                    if nearby_keys:
                        typo_char = random.choice(nearby_keys)
                        pyautogui.write(typo_char)
                        time.sleep(self.config["typing_speed"]["correction_delay"])
                        # Correct the mistake
                        pyautogui.press('backspace')
                        typos += 1
                
                # Type the correct character
                pyautogui.write(current_char)
                
                # Random delay between keystrokes
                delay = random.uniform(
                    self.config["typing_speed"]["min_delay"],
                    self.config["typing_speed"]["max_delay"]
                )
                time.sleep(delay)
                
                i += 1
                pbar.update(1)
        
        avg_speed = total_chars / (pbar.format_dict["elapsed"] or 1)  # Avoid division by zero
        
        if self.verbose:
            print(f"\n{Fore.GREEN}✓ Typing completed successfully{Style.RESET_ALL}")
            print(f"  {Fore.BLUE}• Characters typed: {Fore.CYAN}{total_chars}{Style.RESET_ALL}")
            print(f"  {Fore.BLUE}• Elapsed time: {Fore.CYAN}{pbar.format_dict['elapsed']:.2f}s{Style.RESET_ALL}")
            print(f"  {Fore.BLUE}• Average speed: {Fore.CYAN}{avg_speed:.2f}{Fore.BLUE} chars/sec{Style.RESET_ALL}")
            print(f"  {Fore.BLUE}• Typos made: {Fore.CYAN}{typos}{Style.RESET_ALL}")
            print(f"  {Fore.BLUE}• Pauses taken: {Fore.CYAN}{pauses}{Style.RESET_ALL}")
        
        return True