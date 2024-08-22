import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!

def match_character_groups(input_line, pattern):
    if len(pattern) > 0 and pattern[0] == '^':
        for ch in pattern[1:]:
            if ch in input_line:
                return False
        return True
    else:
        for ch in pattern:
            if ch in input_line:
                return True
        return False

def handle_backslash(input_line, pattern, ii, pi):
    if pattern[pi + 1] == 'd':
        if not input_line[ii].isdigit():
            return None
    if pattern[pi + 1] == 'w':
        if not input_line[ii].isalnum():
            return None
    return ii + 1, pi + 2

def handle_literals(input_line, pattern, ii, pi):
    if pi == len(pattern) - 1:
        return True
    if ii == len(pattern) - 1:
        return False
    if pattern[pi] == '.':
        return ii + 1, pi + 1
    if pattern[pi] == '(':
        i = pi
        while pattern[i] != ')':
            i += 1
        words = pattern[pi + 1 : i].split('|')
        for word in words:
            if input_line[ii: ii + len(word)] == word:
                if handle_literals(input_line, pattern, ii + len(word), i + 1):
                    return True
        return False
    if pattern[pi] != input_line[ii]:
        return None
    return ii + 1, pi + 1

def handle_quantifiers(input_line, pattern, ii, pi):
    if pattern[pi + 1] == '+':
        if pattern[pi] != input_line[ii]:
            return None
        while ii < len(input_line) and pattern[pi] == input_line[ii]:
            ii += 1
        return ii, pi + 2
    
    elif pattern[pi + 1] == '?':
        if pattern[pi] != input_line[ii]:
            return ii, pi + 2
        if ii + 1 >= len(input_line):
            return ii, pi + 2
        if input_line[ii + 1] == pattern[pi]:
            return None
        return ii + 1, pi + 2

def match_character_classes(input_line, pattern):
    ii = pi = 0
    while pi < len(pattern) and ii < len(input_line):
        if pattern[pi] == "\\":
            try:
                ii, pi = handle_backslash(input_line, pattern, ii, pi)
            except TypeError:
                raise TypeError("Invalid")
        elif pi + 1 < len(pattern) and pattern[pi + 1] in ['+', '?']:
            try:
                ii, pi = handle_quantifiers(input_line, pattern, ii, pi)
            except TypeError:
                raise TypeError("Invalid")
        else:
            try:
                ii, pi = handle_literals(input_line, pattern, ii, pi)
            except TypeError:
                raise TypeError("Invalid")

    if pi != len(pattern):
        return False
    return True

def match_pattern(input_line, pattern):
    if len(pattern) > 0 and pattern[0] == '[':
        return match_character_groups(input_line, pattern[1:-1])
    if len(pattern) > 0 and pattern[0] == '^':
        return input_line.startswith(pattern[1:])
    if len(pattern) > 0 and pattern[-1] == '$':
        return input_line.endswith(pattern[:-1])
    else:
        for i in range(len(input_line)):
            try:
                if match_character_classes(input_line[i:], pattern):
                    return True
            except TypeError:
                continue
        return False

def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    print("Logs from your program will appear here!")

    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
