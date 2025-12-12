import sys
import os

def main():

    # Wait for user input
    while True:
        sys.stdout.write("$ ")
        command = input().strip()
        parts = command.split(maxsplit=1)
        cmd = parts[0]
        path = os.getenv("PATH", "")    #returned as string
        dirs = path.split(os.pathsep)
        found_executable = False

        if cmd == "exit":
            break
        elif cmd == "echo":
            if len(parts) > 1:
                print(parts[1])
            else:
                print("")
        elif cmd == "type":
            if len(parts) ==2 :
                if parts[1] in ("echo", "exit", "type"):
                    print(f"{parts[1]} is a shell builtin")
                    continue
                
                #there could be multiple path elements.
                #for each element we need to check each dir
                for directory in dirs:
                    full_file_path = os.path.join(directory, parts[1])
                    if os.path.isfile(full_file_path) and os.access(full_file_path, os.X_OK):
                        print(f"{parts[1]} is {full_file_path}")  
                        found_executable = True
                        break
                    
                if not found_executable:
                    print(f"{parts[1]}: not found")
        else:
            print(f"{command}: command not found")
    pass


if __name__ == "__main__":
    main()
