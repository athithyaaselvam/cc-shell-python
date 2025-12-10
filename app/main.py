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
        elif cmd == "echo":
            if len(parts) > 1:
                print(parts[1])
            else:
                print("")
        elif cmd == "type":
            if len(parts) <=2 :
                if parts[1] in ("echo", "exit", "type"):
                    print(f"{parts[1]} is a shell builtin")
                else:
                    print(f"{parts[1]}: not found")
        else:
            print(f"{command}: command not found")
    pass


if __name__ == "__main__":
    main()
