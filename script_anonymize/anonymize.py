from sql_parse import send_schema, send_change
from change_to_class import prepare_change
from change_file import change_file

import sys
import os
import time


def clean_table(table, change):
    new_t = []
    for t in table:
        tmp = t.split("\n", 1)
        for c in change.keys():
            if c in tmp[0]:
                new_t.append(t.split("\n"))
    return new_t


def usage():
    print("Usage:\tpy anonymize.py FILE \"SCHEMA:PARAMETER\"\n"
          + "\n\tAnonymized every SCHEMA 's PARAMETER in the FILE\n"
          + "\tFILE must be a SQL file (.sql)\n"
          + "\tMUST have at least ONE key-item \"SCHEMA:PARAMETER\"\n"
          + "\n\t-c, copy the file and create a new one anonymized")
    sys.exit(2)


if __name__ == "__main__":
    total = time.time()
    if len(sys.argv) < 3:
        usage()
    if sys.argv[1][:-4] != ".sql" and not os.path.isfile(sys.argv[1]):
        usage()
    start = time.time()
    schema, sql_file, table = send_schema()
    print("func: send schema = " + str(time.time() - start))
    if schema:
        start = time.time()
        change = send_change(schema)
        table = clean_table(table, change)
        print("func: send change = " + str(time.time() - start))
        if change:
            type_to_change = prepare_change(change, table)
            change_file(type_to_change, sql_file)
        else:
            print("No key-items to anonymize")
            sys.exit(2)
    print("temps total : " + str(time.time() - total))
