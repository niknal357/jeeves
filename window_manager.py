"""
Jeeves - Human-like browser typing automation
Window handling functionality
"""

import pygetwindow as gw
import time
import colorama
from colorama import Fore, Style

def find_browser_window(window_title, window_index=0, verbose=True):
    """
    Find and activate a browser window.
    
    Args:
        window_title (str): The title to search for in window titles
        window_index (int): Which window to use if multiple are found
        verbose (bool): Whether to print verbose output
    
    Returns:
        window: The activated window object or None if no window found
    """
    if verbose:
        print(f"{Fore.BLUE}ℹ Searching for windows with title containing '{window_title}'...{Style.RESET_ALL}")
    
    windows = gw.getWindowsWithTitle(window_title)
    
    if not windows:
        print(f"{Fore.RED}✗ No windows with title containing '{window_title}' found.{Style.RESET_ALL}")
        return None
    
    if verbose and len(windows) > 1:
        print(f"{Fore.BLUE}ℹ Found {len(windows)} matching windows:{Style.RESET_ALL}")
        for i, win in enumerate(windows):
            marker = "→ " if i == window_index else "  "
            print(f"  {marker}{i}: {win.title}")
    
    if window_index >= len(windows):
        print(f"{Fore.YELLOW}⚠ Window index {window_index} is out of range. Using first window instead.{Style.RESET_ALL}")
        window_index = 0  # Default to first window
    
    selected_window = windows[window_index]
    window_title = selected_window.title
    
    try:
        if verbose:
            print(f"{Fore.BLUE}ℹ Activating window: {Fore.CYAN}{window_title}{Style.RESET_ALL}")
        selected_window.activate()
        return selected_window
    except Exception as e:
        print(f"{Fore.RED}✗ Error activating window: {e}{Style.RESET_ALL}")
        return None

def list_browser_windows():
    """
    List all visible windows for the user to choose from.
    
    Returns:
        list: A list of all active windows
    """
    windows = gw.getAllWindows()
    active_windows = [w for w in windows if w.visible]
    
    print(f"{Fore.CYAN}Available windows:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'Index':<6} {'Title':<50}{Style.RESET_ALL}")
    
    for i, window in enumerate(active_windows):
        if i % 2 == 0:
            print(f"{Fore.WHITE}{i:<6} {window.title[:50]}{Style.RESET_ALL}")
        else:
            print(f"{Fore.BLUE}{i:<6} {window.title[:50]}{Style.RESET_ALL}")
    
    return active_windows