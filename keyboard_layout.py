def get_nearby_keys(char):
    """Get keys that are physically near the given character on a QWERTY keyboard."""
    keyboard_layout = {
        'q': ['w', 'a', '1'],
        'w': ['q', 'e', 'a', 's', '2'],
        'e': ['w', 'r', 's', 'd', '3'],
        'r': ['e', 't', 'd', 'f', '4'],
        't': ['r', 'y', 'f', 'g', '5'],
        'y': ['t', 'u', 'g', 'h', '6'],
        'u': ['y', 'i', 'h', 'j', '7'],
        'i': ['u', 'o', 'j', 'k', '8'],
        'o': ['i', 'p', 'k', 'l', '9'],
        'p': ['o', '[', 'l', ';', '0'],
        'a': ['q', 'w', 's', 'z'],
        's': ['w', 'e', 'a', 'd', 'z', 'x'],
        'd': ['e', 'r', 's', 'f', 'x', 'c'],
        'f': ['r', 't', 'd', 'g', 'c', 'v'],
        'g': ['t', 'y', 'f', 'h', 'v', 'b'],
        'h': ['y', 'u', 'g', 'j', 'b', 'n'],
        'j': ['u', 'i', 'h', 'k', 'n', 'm'],
        'k': ['i', 'o', 'j', 'l', 'm', ','],
        'l': ['o', 'p', 'k', ';', ',', '.'],
        'z': ['a', 's', 'x'],
        'x': ['z', 's', 'd', 'c'],
        'c': ['x', 'd', 'f', 'v'],
        'v': ['c', 'f', 'g', 'b'],
        'b': ['v', 'g', 'h', 'n'],
        'n': ['b', 'h', 'j', 'm'],
        'm': ['n', 'j', 'k', ','],
        ' ': ['c', 'v', 'b', 'n', 'm']
    }
    
    char = char.lower()
    if char in keyboard_layout:
        # match case of input character
        return [key.upper() if char.isupper() else key for key in keyboard_layout[char]]
    return []