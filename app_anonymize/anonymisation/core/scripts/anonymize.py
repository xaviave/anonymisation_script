from anonymisation.core.scripts.sql_parse import send_schema, send_change, clean_table
from anonymisation.core.scripts.change_to_class import prepare_change
from anonymisation.core.scripts.change_file import change_file
from anonymisation.core.scripts.generate_file import generate_db

import sys
import time
import re


def dict_to_list(lst_change):
    change = []
    for name in lst_change:
        if isinstance(lst_change[name], list):
            for table in lst_change[name]:
                change.append("%s:%s" % (name, table))
        elif isinstance(lst_change[name], str):
                change.append("%s:%s" % (name, lst_change[name]))
    return change


def run(document, lst_change, type_change, nb_insert):
    path = "error"
    create = re.compile(r"(create|CREATE)(\s)+(table|TABLE)")
    insert = re.compile(r"(insert|INSERT)(\s)+(into|INTO)")
    schema, sql_file, table = send_schema(document, create, insert)
    name_file = ""
    if schema:
        start = time.time()
        if type_change == 0:
            change = send_change(schema, dict_to_list(lst_change))
        else:
            change = dict(schema)
        table = clean_table(table, change)
        print("func: send change = " + str(time.time() - start))
        if change:
            type_to_change = prepare_change(change, table)
            name_file = document.document.name
            name_file = name_file[name_file.find('/') + 1:name_file.find('.')]
            if type_change == 0:
                name_file += "_anonymize.sql"
                path = change_file(type_to_change, sql_file, name_file, insert)
            else:
                name_file += "_generate.sql"
                path = generate_db(type_to_change, sql_file, nb_insert, create, name_file)
        else:
            print("No key-items to anonymize")
            sys.exit(2)
    return name_file, path
