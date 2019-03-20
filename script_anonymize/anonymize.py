from sql_parse import send_schema, send_change, clean_table
from change_to_class import prepare_change
from generate_file import generate_db
from change_file import change_file

import sys
import os
import time
import re


def usage():
    print("Usage:\tanonymize.py\n\n\tAnonymizer : \n\t\tpy anonymize.py FILE \"SCHEMA:PARAMETER\"\n"
          + "\n\t\tAnonymized every SCHEMA 's PARAMETER in the FILE\n"
          + "\t\tFILE must be a SQL file (.sql)\n"
          + "\t\tMUST have at least ONE key-item \"SCHEMA:PARAMETER\"\n"
          + "\n\n\tGenerator :\n\t\tpy anonymize.py FILE -g [NB_INSERT]\n"
          + "\n\t\tgenerate an sql file with the SCHEMA provided"
          + "\n\t\t(don't generate link KEY for now) \n")
    sys.exit(2)


def return_sys_av(arg):
    if arg in sys.argv:
        for x, av in enumerate(sys.argv):
            if av == arg and x + 1 < len(sys.argv):
                return sys.argv[x + 1]
    else:
        usage()


if __name__ == "__main__":
    total = time.time()
    if len(sys.argv) < 3:
        usage()
    if sys.argv[1][:-4] != ".sql" and not os.path.isfile(sys.argv[1]):
        usage()
    nb_insert = -1
    all_db = 0
    if "-g" in sys.argv:
        argv = return_sys_av("-g")
        if argv and argv.isdigit() > 0:
            nb_insert = int(argv)
        else:
            usage()
    elif "-a" in sys.argv:
        all_db = 1
    create = re.compile(r"(create|CREATE)(\s)+(table|TABLE)")
    insert = re.compile(r"(insert|INSERT)(\s)+(into|INTO)")
    schema, sql_file, table = send_schema(create, insert)
    if schema:
        if nb_insert > 0 or all_db == 1:
            change = dict(schema)
        else:
            change = send_change(schema)
        table = clean_table(table, change)
        if change:
            type_to_change = prepare_change(change, table)
            if nb_insert > 0:
                generate_db(type_to_change, sql_file, nb_insert, create)
            else:
                change_file(type_to_change, sql_file, insert)
        else:
            print("No key-items to anonymize")
            sys.exit(2)
    print("temps total anonymize : " + str(time.time() - total) + " sec")
    print("temps total anonymize : " + str((time.time() - total) / 60) + " min")
