import sys

from imshare.build import build
from imshare.gen_config import gen_nginx_conf


def main(argv: list[str]):
    argv.pop(0)  # pop the program name from argv
    match argv:
        case ["build"]:
            build()
        case ["gen-config", cfg]:
            if cfg.lower() == "nginx":
                gen_nginx_conf()
            else:
                print("Unknown configuration provider")
                return 1
        case invalid:
            print_help()
            return 0 if invalid == ["help"] else 1
    return 0


def print_help():
    print(
        """imshare: Simple, static image sharing
          
USAGE:
          
          imshare <COMMAND> <ARGUMENTS>

COMMAND:
          
    build           
                    (re)build the static files

    gen-config <provider>
                    Generate a configuration file for a specific
                    provider. Supported providers are: nginx
"""
    )


if __name__ == "__main__":
    sys.exit(main(sys.argv))
