__\<Disclaimer\>__

The programs provided herein are __not__ extensively tested. If you use them to
send email messages containing your expenses reports, I strongly recommend that
you don't address them directly to "uninterested parties". At least until these
utilities have seen some more use, send emails to a personal address where you
can check the validity of their contents before forwarding them along to others.

__\<Disclaimer\/\>__

## Overview
`evuber` provides a suite of programs to retrieve, prepare, and send materials
for Uber expenses at Evertz. They can be used to:
- Download Uber trip summary emails in a given date range,
- convert trip summaries into ready-to-submit weekly expense reports,
  with a filled-in expense form and receipt PDFs, and
- send expense reports as email attachments to an address of your choosing.

## Installation and Setup

1. Clone
```bash 
$ git clone https://github.com/andkerr/evuber.git
$ cd evuber
```

2. Install the `evuber` executable and its dependencies
```bash
$ sudo ./install
```

3. Set up your fetching and forwarding addresses, and other details
```bash 
$ evuber configure
```

4. Put a blank copy of the Evertz expense form template named `template.xlsx` in
   `$HOME/.evuber`.

## Usage

Most `evuber` commands produce output that can be used as input to subsequent
programs, and many commands will read their positional arguments from the
standard input if none are provided on the command line, so programs can easily
be piped together. For example, the pipeline
```bash 
$ evuber fetch | evuber scrape | evuber send
```
will convert all the Uber trip summaries ever sent to your email into weekly
expense reports, and attach each report to a separate email.

Running `evubuer help` prints a list of available commands and a short
description for each. Use `evuber <command> --help` to see more a more detailed
description of a command, plus options that can further specify its behaviour.

## Configuration

Before it can process Uber receipts and expense reports `evuber` needs to know
things like where to fetch your trip summary emails from, and what information
to populate the expense form template with.

    - NAME
    - DEPT
    - MANAGER
    - ADDRESSLINE1
    - ADDRESSLINE2
    - FETCH_ADDRESS
    - FETCH_IMAP
    - FETCH_SMTP
    - FETCH_PASSWORD
    - SEND_ADDRESS

By default, `evuber` looks for configuration variables in
`~/.evuber/config.json`. Re-running `evuber configure` or manually editing
`config.json` will update your settings.

Environment variables take precendence over file-based configuration, so a
command like
```bash 
FETCH_ADDRESS=me@example.com evuber fetch
```
will fetch trip summary emails sent to me@example, regardless of what address is
set in your `config.json` file.

### A note on email credentials

Some email services that use 2FA (e.g. Gmail, Outlook), disallow using your
regular password to access messages programatically. In this case, you will
likely have to create an [app password](https://www.google.com/search?client=firefox-b-d&q=email+app+password)
to pass to `evuber`'s FETCH_PASSWORD configuration variable.

### A further note on email

So far, I have not found a way to fetch emails from evert.com email addresses.
If you manage to get one working, please let me know.
