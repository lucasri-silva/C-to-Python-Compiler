import re

def lexical_analysis():
    file = "Cprogram.c"
    characters_set = set()
    
    with open(file, "r") as file:
    
        while True:
            char = file.read(1)
            if char.strip():
                characters_set.add(char)
            if not char: # end of file
                break

    valid_characters = r"[A-Za-z0-9_+\-*/%<>=!&|\"'`‘“@^\$#~?:,;.(){}[\]\t\n\r\\]"
    invalid_characters = []

    for character in characters_set:
        if not re.findall(valid_characters, character):
            invalid_characters.append(character)
            print(f"Invalid character found: {character}")
    
    return 1 if invalid_characters else 0