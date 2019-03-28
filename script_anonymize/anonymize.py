from sql_parse import send_schema, send_change, clean_table, send_schema_wid
from change_to_class import prepare_change
from generate_file import generate_db
from change_file import change_file

import sys
import os
import time
import re


def usage():
    print("Usage:\tanonymize.py\n\n\tAnonymizer : \n\t\tpy anonymize.py FILE \"TABLE:PARAMETER[=STATIC_VAR]\"\n"
          + "\n\t\tAnonymized every TABLE 's PARAMETER in the FILE\n"
          + "\t\tFILE must be a SQL file (.sql)\n"
          + "\t\tMUST have at least ONE key-item \"TABLE:PARAMETER\"\n\n"
          + "\t\t[=STATIC_VAR]\tput STATIC_VAR in all the PARAMETER\n"
          + "\t\t\t\tif the STATIC_VAR isn't in an ENUM PARAMETER,\n"
          + "\t\t\t\tthe PARAMETER is NOT anonymized\n"
          + "\t\t\t-f\tforce all the anonimization with STATIC_VAR even\n"
          + "\t\t\t\tif the STATIC_VAR isn't valid in an ENUM,\n"
          + "\t\t\t\tit chooses a random value in the ENUM\n"
          + "\n\t\t-a\tselect all the parameter in the table\n"
          + "\n\t\t-id\t(just with -a) select all the parameter except the ID in the table\n"
          + "\t\t\tno need \"SCHEMA:PARAMETER\" args\n"
          + "\n\n\tGenerator :\n\t\tpy anonymize.py FILE -g [NB_INSERT]\n"
          + "\n\t\t[NB_INSERT] : number of line generated for all table\n"
          + "\n\t\tgenerate an sql file with the SCHEMA provided"
          + "\n\t\t(don't generate KEY for now) \n")
    sys.exit(2)


def return_sys_av(arg):
    if arg in sys.argv:
        for x, av in enumerate(sys.argv):
            if av == arg and x + 1 < len(sys.argv):
                return sys.argv[x + 1]
    else:
        usage()


def send_option():
    nb = -1
    all_db = 0
    if "-g" in sys.argv:
        argv = return_sys_av("-g")
        if argv and argv.isdigit() > 0:
            nb = int(argv)
        else:
            usage()
    elif "-a" in sys.argv:
        if "-id" in sys.argv:
            all_db = 2
        else:
            all_db = 1
    return nb, all_db


if __name__ == "__main__":
    total = time.time()
    if len(sys.argv) < 3:
        usage()
    if sys.argv[1][:-4] != ".sql" and not os.path.isfile(sys.argv[1]):
        usage()
    nb_insert, all_db = send_option()
    create = re.compile(r"(create|CREATE)(\s)+(table|TABLE)")
    insert = re.compile(r"(insert|INSERT)(\s)+(into|INTO)")
    schema, sql_file, table = send_schema(create, insert)
    if schema:
        if nb_insert > 0 or all_db == 1:
            change = dict(schema)
        elif all_db == 2:
            change = send_schema_wid(schema)
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
    print("\ntemps total anonymize : " + str(time.time() - total) + " sec")
    print("temps total anonymize : " + str((time.time() - total) / 60) + " min")
