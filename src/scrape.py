import argparse
import logging
from pathlib import Path
import sys

from libreceipt import CONFIG_DIR, emit, group_weeks, parse_trip


def main():
    parser = argparse.ArgumentParser(description="Scrape Uber receipts into Evertz expense forms",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("files",
                        type=str,
                        metavar="FILE",
                        nargs="*",
                        help="PDF or HTML files to scrape. If there are no " \
                             "FILE arguments, filenames are read from the " \
                             "standard input.")
    parser.add_argument("-c",
                        "--clean",
                        action="store_true",
                        help="Delete input files after processing")
    parser.add_argument("-t",
                        "--template",
                        type=Path,
                        default=(CONFIG_DIR / "template.xlsx"),
                        help="Expense form template")
    parser.add_argument("-v",
                        "--verbose",
                        action="store_true",
                        help="Print debug output to stderr")
    parser.add_argument("--with-address",
                        action="store_true",
                        help="Include your mailing address in expense forms. " \
                             "HR only requires this if it changed since your " \
                             "last expense report.")
    args = parser.parse_args()

    log = logging.getLogger("libreceipt")
    if args.verbose:
        log.setLevel(logging.INFO)

    if not args.template.exists():
        log.error(f"Could not find expense form at {args.template}")
        sys.exit(1)

    if args.files:
        # this handles no-match globs, which the shell does not expand (to the
        # empty string) unless the nullglob option is set (shopt -s nullglob)
        files = [path for pattern in args.files for path in Path().glob(pattern)]
    else:
        files = [Path(line.rstrip()) for line in sys.stdin]

    trips = [parse_trip(receipt) for receipt in files]
    if len(set((t.date, t.time) for t in trips)) != len(trips):
        log.error("[error] Input contains multiple trips at the same date and time")
        sys.exit(1)

    for wkstart, trips in group_weeks(trips):
        print(emit(wkstart, trips, args.template, args.with_address))

    if args.clean:
        for file in files:
            file.unlink()


if __name__ == "__main__":
    main()
