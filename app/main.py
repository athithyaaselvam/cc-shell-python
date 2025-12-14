import sys
import os
import subprocess


# ---------- Builtins ----------
def builtin_echo(args: list[str]) -> None:
    print(' '.join(args))


def builtin_pwd(args: list[str]) -> None:
    print(os.getcwd())


def builtin_cd(args: list[str]) -> None:
    if len(args) != 1:
        print("cd takes exactly one argument")
        return

    target = os.getenv("HOME", "") if args[0] == "~" else args[0]
    try:
        os.chdir(target)
    except FileNotFoundError:
        print(f"cd: {args[0]}: No such file or directory")
    except NotADirectoryError:
        print(f"cd: {args[0]}: Not a directory")


def builtin_type(args: list[str], builtins: dict) -> None:
    if len(args) != 1:
        return

    name = args[0]

    # 1) Builtin?
    if name in builtins or name in ("exit", "type") :
        print(f"{name} is a shell builtin")
        return

    # 2) Search PATH
    path = os.getenv("PATH", "")
    dirs = path.split(os.pathsep) if path else []

    for d in dirs:
        if not d:
            continue
        candidate = os.path.join(d, name)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            print(f"{name} is {candidate}")
            return

    # 3) Not found
    print(f"{name}: not found")


# Builtin registry
BUILTINS = {
    "echo": builtin_echo,
    "pwd": builtin_pwd,
    "cd": builtin_cd,
    # "type" is handled with special signature below
}


def find_executable(cmd: str) -> str | None:
    path = os.getenv("PATH", "")
    dirs = path.split(os.pathsep) if path else []

    for d in dirs:
        if not d:
            continue
        candidate = os.path.join(d, cmd)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return cmd
    return None


def main() -> None:
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        try:
            command_line = input().strip()
        except EOFError:
            break

        parts = command_line.split()
        if not parts:
            continue

        cmd = parts[0]
        args = parts[1:]

        # exit
        if cmd == "exit":
            break

        # type (special builtin, needs builtins registry)
        if cmd == "type":
            builtin_type(args, BUILTINS)
            continue

        # other builtins
        if cmd in BUILTINS:
            BUILTINS[cmd](args)
            continue

        # external commands
        exe_path = find_executable(cmd)
        if exe_path is None:
            print(f"{command_line}: command not found")
            continue

        subprocess.run([exe_path] + args)


if __name__ == "__main__":
    main()
