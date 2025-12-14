import sys
import os
import subprocess

def main():

    # Wait for user input
    while True:
        sys.stdout.write("$ ")
        command = input().strip()
        parts = command.split()
        if not parts:
            continue
        cmd = parts[0]
        args = parts[1:]
        path = os.getenv("PATH", "")    #returned as string
        dirs = path.split(os.pathsep)
        found_executable = False

        if cmd == "exit":
            break
        
        elif cmd == "echo":
            if len(parts) > 1:
                print(" ".join(args))
            else:
                print("")
        
        elif cmd == "type":
            if len(parts) ==2 :
                if parts[1] in ("echo", "exit", "type", "pwd", "cd"):
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
        
        elif cmd == "pwd":
            # if args is None:
                # sys.stdout.write(f"{os.getcwd()}")
            print(f"{os.getcwd()}")

        elif cmd == "cd":
            #check if the given path is one arg
            #check if that arg location exits from pwd or check abs path
            #if exits, switch to that location
            #absolute path
            if args[0][0] == "/" and os.path.isdir(args[0]) and len(args) == 1:
                os.chdir(args[0])
            else:
                print(f"{cmd}: {args[0]}: No such file or directory")    



        else:
            for directory in dirs:
                full_command_path = os.path.join(directory, parts[0])
                if os.path.isfile(full_command_path) and os.access(full_command_path, os.X_OK):
                    subprocess.run([parts[0]] + args)
                    break

            else:
                print(f"{command}: command not found")
    pass


if __name__ == "__main__":
    main()
