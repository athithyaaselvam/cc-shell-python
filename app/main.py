import sys


def main():

    # Wait for user input
    while True:
        sys.stdout.write("$ ")
        command = input().strip()
        parts = command.split(maxsplit=1)
        cmd = parts[0]
        if cmd == "exit":
            break
        if cmd == "echo":
            if len(parts[1]) > 1:
                print(parts[1])
            else:
                print("") 
        else:
            print(f"{command}: command not found")
    pass


if __name__ == "__main__":
    main()
