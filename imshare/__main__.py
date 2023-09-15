import sys

from imshare.build import build

def main(argv: list[str]):
    argv.pop(0)  # pop the program name from argv
    if argv == ["build"]:
        return build()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
