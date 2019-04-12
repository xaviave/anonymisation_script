from anonymisation.core.scripts.sql_parse import send_schema, send_change, clean_table, send_schema_wid
from anonymisation.core.scripts.change_to_class import prepare_change
from anonymisation.core.scripts.change_file import change_file
from anonymisation.core.scripts.generate_file import generate_db
#from anonymisation.core.views import home

import time
import re


def send_id(i, schema, lst):
    for j, s in enumerate(lst):
        if s == schema[i]:
            return j
    return -1


def q_to_dict(request, schema):
    dic = {}
    for k, v in request.POST.lists():
        if k != "all_db" and k != "force" and k != "nb_insert":
            if k in schema.keys():
                if len(v) == 1:
                    dic[k] = v[0]
                else:
                    dic[k] = v
    for k, v in request.POST.lists():
        if k != "all_db" and k != "force" and k != "nb_insert" and k not in schema.keys():
            if k[-6:] == "_force" and k[:-6] in schema.keys():
                for i, change in enumerate(v):
                    if change:
                        id = send_id(i, schema[k[:-6]], dic[k[:-6]])
                        if id != -1:
                            dic[k[:-6]][id] += "=" + change
    return dic


def dict_to_list(lst_change):
    change = []
    for name in lst_change:
        if isinstance(lst_change[name], list):
            for table in lst_change[name]:
                change.append("%s:%s" % (name, table))
        elif isinstance(lst_change[name], str):
                change.append("%s:%s" % (name, lst_change[name]))
    return change


def run(document, request, type_change, nb_insert, all_db, force):
    path = "error"
    name_file = document.document.name
    create = re.compile(r"(create|CREATE)(\s)+(table|TABLE)")
    insert = re.compile(r"(insert|INSERT)(\s)+(into|INTO)")
    schema, sql_file, table_row = send_schema(document, create, insert)
    if type_change == 0:
        lst_change = q_to_dict(request, schema)
    if schema:
        start = time.time()
        if nb_insert > 0 or all_db == 1:
            change = dict(schema)
        elif all_db == 2:
            change = send_schema_wid(schema)
        else:
            change = send_change(schema, dict_to_list(lst_change))
        table, table_row = clean_table(table_row, change)
        print("func: send change = " + str(time.time() - start))
        if change:
            type_to_change = prepare_change(change, table, force, table_row)
            name_file = name_file[name_file.find('/') + 1:name_file.find('.')]
            if type_change == 0:
                name_file += "_anonymized.sql"
                change_file(type_to_change, sql_file, name_file, insert)
            else:
                name_file += "_generated.sql"
                generate_db(type_to_change, sql_file, nb_insert, create, name_file)
        else:
            print("No key-items to anonymize")
            #return home(request)
    return name_file
