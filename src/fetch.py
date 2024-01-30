import argparse
import datetime
import logging
import os
import sys

from libreceipt import getconfig, trip_summaries


def main():
    parser = argparse.ArgumentParser(description="Fetch HTML receipts from Uber trip summary emails",
                                     epilog=datefmthelp,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--since",
                        type=rfc2822date,
                        help="Fetch trip summary emails set on or after this date")
    parser.add_argument("--until",
                        type=rfc2822date,
                        nargs="?",
                        help="Fetch trip summary emails sent before this date")
    parser.add_argument("-v",
                        "--verbose",
                        action="store_true",
                        help="Print debug output to stderr")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger("libreceipt").setLevel(logging.INFO)

    addr =   getconfig("FETCH_ADDRESS")
    passwd = getconfig("FETCH_PASSWORD")
    imap =   getconfig("FETCH_IMAP")
    if not addr or not passwd:
        logging.error("Failed to read email login credentials from the environment")
        sys.exit(1)

    for uid, html in trip_summaries(addr, passwd, imap, args.since, args.until):
        dst = f"evuber_{uid}.html"
        print(dst)
        with open(dst, "w") as f:
            f.write(html.rstrip())


datefmthelp = """\
Date arguments must match <day_text>-<month_text>-<year_text>, where
  <day_text>   is the 2-digit day of the month (e.g. 08)
  <month_text> is the 3-letter, capitalized month (e.g Jan)
  <year_text>  is the 4-digit year (e.g. 2024)

This matches the Unix strftime format string "%d-%b-%Y", which can be
passed to e.g. the date command to produce dates compatible with fetch.
"""


def rfc2822date(date: str):
    try:
        datetime.datetime.strptime(date, "%d-%b-%Y")
    except Exception:
        raise ValueError
    return date


if __name__ == "__main__":
    main()
