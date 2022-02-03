import sys
import json
import time
import datetime
import dateutil.parser

def parse_command_line():
    if len(sys.argv) != 2:
        raise Exception("Usage: <meta_data_file>")

    return sys.argv[1]

def load_file(path):
    with open(path, "r") as f:
        return json.load(f)

def main():
    meta_data_file = parse_command_line()
    data = load_file(meta_data_file)

    if "late_due_date" in data["assignment"]:
        due_date = data["assignment"]["late_due_date"]
    else:
        due_date = data["assignment"]["due_date"]

    unix_due_date = dateutil.parser.isoparse(due_date).timestamp()

    if time.time() < unix_due_date:
        print("true")
    else:
        print("false")


if __name__ == "__main__":
    main()
