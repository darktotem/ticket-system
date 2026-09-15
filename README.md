# Customer Care Ticket System

A small CLI app for handling customer support tickets. 
There are three kinds of people who use it, the customers, the customer care employees, and
themanagers.
Everything is saved to a plain JSON files.

## What's in here

ticket_system/
- main.py                    # run this to start the app
- requirements.txt

models/
- user.py                 # a customer
- employee.py             # a customer care agent (extends User)
- manager.py               # oversees everything (extends User)
- ticket.py                 # a support ticket + its history log

utils/
- auth.py                  # registering and logging in
- decorators.py            # checks like "must be logged in", "must be an employee"
- storage.py                # reading/writing the JSON files
- validators.py             # basic checks like "is this a real email"
- ticket_manager.py         # everything to do with creating/updating tickets
tests/
- test_user.py
- test_employee.py
- test_manager.py
- test_ticket.py
- test_auth.py
- test_tickets.py
- test_cli.py

data/
- users.json                # gets created the first time you run the app
- tickets.json


## The three roles

- **Customer** — signs up, describes their problem, gets a ticket number
  back. Later, they say whether the fix actually worked.

- **Employee** — looks up a ticket by its number, leaves a note on what
  they're doing about it, or marks it as resolved.

- **Manager** — can see every ticket and every employee, no matter who's
  working on what.

## How a ticket moves through the system

open -> pending -> closed

- **open** — just came in, nobody's touched it yet.

- **pending** — someone's working on it, or the customer said it's not
  actually fixed yet and it's bounced back.

- **closed** — the customer confirmed the issue is actually resolved.

Every ticket keeps a running log of everything that's happened to it,
who did what, and when.
if one employee starts working a ticket and then can't finish it, whoever picks it up next can open the ticket by number and see exactly what was already tried, instead of starting from scratch.

## Getting it running on your machine

You'll need Python 3.10 or newer already installed. 
Everything else below gets installed for you.

1. Open a terminal in the project folder.

2. Create a virtual environment. 
This just keeps this project's installed packages separate from everything else on your machine, so you don't end up with version conflicts down the line.

type on the terminal

python3 -m venv venv

3. Turn the virtual environment on.

type on the terminal

source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

You'll know it worked because your terminal prompt will now start with
"(venv)"

4. Install the two things this project actually needs.

type on the terminal

pip install -r requirements.txt

This installs:
- **rich** — makes the terminal output look nice (colored text, tables,
  boxes) instead of plain print statements
- **pytest** — runs the automated tests

## Running the app

Type on the terminal

python main.py

You'll land on a menu to register or log in. A good first test run:
register once as a customer, log out, register again as an employee, log
out, register a third time as a manager, then try logging in as each one
and clicking through their menu to see what each role can do.

Everything you do is saved to `data/users.json` and `data/tickets.json`,
so if you close the app and reopen it, your accounts and tickets are
still there.

## Checking that everything actually works

Before you trust any of this, run the test suite:

type on the terminal

pytest

If everything's set up correctly you should see something like "35
passed" with no red text. If a test fails, that's your signal something's
broken, fix it before building on top of it, don't just ignore it.

## NOTE

- Passwords are hashed with SHA-256 not bcrypt or passlib
- Outside of `rich` and `pytest`, this project doesn't depend on anything
  else. No 
  It doesn't have any web framework or database driver nothing
