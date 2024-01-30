import argparse
import logging
import os
from pathlib import Path
import shutil
import sys

from libreceipt import getconfig, senddir


def main():
    parser = argparse.ArgumentParser(description="Attach directory contents to Evertz expense emails")
    parser.add_argument("dirs",
                        type=str,
                        metavar="DIRS",
                        nargs="*",
                        help="Directories to attach in separate emails")
    parser.add_argument("-c",
                        "--clean",
                        action="store_true",
                        help="Delete input directories after processing")
    parser.add_argument("-n",
                        "--dry-run",
                        action="store_true",
                        help="Don't actually send emails, just show what would be sent")
    parser.add_argument("-v",
                        "--verbose",
                        action="store_true",
                        help="Print debug output to stderr")
    args = parser.parse_args()

    if args.verbose or args.dry_run:
        logging.getLogger("libreceipt").setLevel(logging.INFO)

    fromaddr = getconfig("FETCH_ADDRESS")
    frompass = getconfig("FETCH_PASSWORD")
    smtp     = getconfig("FETCH_SMTP")
    destaddr = getconfig("SEND_ADDRESS")
    if not fromaddr or not frompass or not destaddr:
        logging.error("Failed to read email credentials from environment")
        sys.exit(1)

    if args.dirs:
        dirs = [path for pattern in args.dirs for path in Path().glob(pattern)]
    else:
        dirs = [Path(line.rstrip()) for line in sys.stdin]

    for d in dirs:
        senddir(d, fromaddr, frompass, destaddr, smtp, args.dry_run)

    if args.clean:
        for d in dirs:
            shutil.rmtree(d)


if __name__ == "__main__":
    main()
