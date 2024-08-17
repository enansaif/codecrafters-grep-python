import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        return pattern in input_line
    elif pattern == r"\d":
        return any(ch.isdigit() for ch in input_line)
    elif pattern == r"\w":
        return any(ch.isalnum() for ch in input_line)
    elif len(pattern) > 0 and pattern[0] == '[':
        for ch in pattern[1:-1]:
            if ch in input_line:
                return True
        return False
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")


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
