# Repair-Tool
> Written by [turtleisaac](https://github.com/turtleisaac)

A tool that (hopefully) will repair data corruption in Gen 4 Pokémon ROMs that has been caused by usage of PPRE

**WIP**

**Don't you dare use this tool's existence as an excuse to use PPRE. This is meant to repair old hacks made using PPRE so they can be edited using modern tools.**

---

## How it works

In a nutshell, this tool goes through specific game files and verifies the length of each file, the contents of each byte within the file, and ensures that each file adheres to the specification for that specific file type.

## Usage

### First time run

Run `pip3 install -r requirements.txt` from terminal in the main directory of this tool.
Then run `python3 Main.py`.

### Otherwise

Run `python3 Main.py`.