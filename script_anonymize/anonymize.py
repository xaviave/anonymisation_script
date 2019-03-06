from sql_parse import send_schema, send_change

import sys
import os
import time


def change_file(schema, chanage, file):
    pass


def usage():
    print("Usage:\tpy anonymize.py FILE \"SCHEMA:PARAMETER\"\n"
          + "\n\tAnonymized every SCHEMA 's PARAMETER in the FILE\n"
          + "\tFILE must be a SQL file (.sql)\n"
          + "\tMUST have at least ONE key-item \"SCHEMA:PARAMETER\"\n"
          + "\n\t-c, copy the file and create a new one anonymized")
    sys.exit(2)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
        sys.exit(2)
    if sys.argv[1][:-4] != ".sql" and not os.path.isfile(sys.argv[1]):
        usage()
        sys.exit(2)
    start = time.time()
    schema, file = send_schema()
    print("func: send schema = ", time.time() - start)
    start = time.time()
    if schema:
        change = send_change(schema)
    print("func: send change = ", time.time() - start)
    print(change)
    """
        
        if change:
            change_file(schema, change, file)
        else:
            print("No key-items to anonymize")
            sys.exit(2)
    else:
        print("The file is not a SQL file or is an invalid one")
        sys.exit(2)
    """
else:
    print(__name__)
