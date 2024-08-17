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

def match_character_classes(input_line, pattern):
    i, j = 0, 0
    while i < len(pattern) and j < len(input_line):
        if pattern[i].isalnum() or pattern[i].isspace():
            if pattern[i] != input_line[j]:
                return False
            i += 1
            j += 1
        else:
            if pattern[i] == 'd':
                if not input_line[j].isdigit():
                    return False
            if pattern[i] == 'w':
                if not input_line[j].isalnum():
                    return False
            i += 2
            j += 1
            
    if i != len(pattern) or j != len(input_line):
        return False
    return True
            

def match_pattern(input_line, pattern):
    if len(pattern) > 0 and pattern[0] == '[':
        return match_character_groups(input_line, pattern[1:-1])
    else:
        return match_character_classes(input_line, pattern)


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
