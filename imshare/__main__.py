import sys
import os
import argparse

from imshare.build import build, process_images, get_shares
from imshare.gen_config import print_nginx_conf
from imshare.export import copy_compressed_with_plain_names_to
import imshare.conf as conf


def main(argv: list[str]):
    # argv.pop(0)  # pop the program name from argv

    parser = argparse.ArgumentParser(
        "imshare", description="simple, static image sharing"
    )

    parser.add_argument(
        "--num-jobs",
        "-j",
        default=None,
        type=int,
        help="Run num jobs simultaneously (for image conversion). Defaults to 8.",
    )
    parser.add_argument(
        "--base-dir",
        "-d",
        default=None,
        type=str,
        help="Run as if inside the following directory",
    )
    args, argv = parser.parse_known_args(argv)

    argv.pop(0)

    conf.CONF = conf.Config(num_jobs=args.num_jobs)

    base_dir = os.environ["PWD"]
    if args.base_dir:
        os.chdir(args.base_dir)

    try:
        match argv:
            case ["build"]:
                build()
            case ["gen-config", cfg]:
                if cfg.lower() == "nginx":
                    print_nginx_conf()
                else:
                    print("Unknown configuration provider")
                    return 1
            case ["export", share, dest]:
                print(f"Exporting share {share} to {dest}")
                copy_compressed_with_plain_names_to(share, dest)
            case ["process", *shares]:
                if not shares:
                    shares = get_shares()
                process_images(shares)
            case invalid:
                print_help()
                return 0 if invalid == ["help"] else 1
        return 0
    finally:
        os.chdir(base_dir)


def print_help():
    print(
        """imshare: Simple, static image sharing
          
USAGE:
          
          imshare <OPTS> <COMMAND> <ARGUMENTS>

COMMAND:
          
    build           
                    (re)build the static files

    export share dest
                    Export the share to the folder dest,
                    copying all processed images.

    process (share*)?
                    Run thumbnail and lower-quality image
                    generation for the web.

    import share *img
                    Create or update share with images.
                    Does not run any processing scripts.

    gen-config <provider>
                    Generate a configuration file for a specific
                    provider. Supported providers are: nginx

OPTS:
    -j <num job>
                    Run num jobs simultaneously (for image conversion).
                    Defaults to 8.

    - d <dir>
                    Change directory to dir before executing the command.
"""
    )


if __name__ == "__main__":
    sys.exit(main(sys.argv))
