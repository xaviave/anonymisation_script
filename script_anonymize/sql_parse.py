import re
import sys
import copy

from functools import reduce


def send_file(doc):
    with open(doc) as fd:
        sql_file = fd.read()
        fd.close()
    return sql_file


def only_table(s):
    li = []
    s = s.split("\n")
    for i, line in enumerate(s):
        if i == 0:
            m = re.search(r"`(.)+`", line)
            if m:
                li.append(m.group()[1:-1])
            else:
                li.append(line.rsplit(' ', 2)[1])
        else:
            m = re.search(r"`(.)+`", line)
            if m and "KEY" not in line and ';' not in line:
                li.append(m.group()[1:-1])
            elif "KEY" not in line and len(line) > 4 and ';' not in line:
                li.append(line.split(' ', 1)[0].strip())
    li = reduce(lambda r, v: v in r[1] and r or (r[0].append(v) or r[1].add(v)) or r, li, ([], set()))[0]
    return li


def clear_schema(schema):
    s = {}
    for i in range(0, len(schema)):
        name = schema[i][0]
        del schema[i][0]
        dic = {}
        for x in range(len(schema[i])):
            dic[x] = schema[i][x]
        s[name] = dic
    return s


def send_schema():
    sql_file = send_file(sys.argv[1]).split(';')
    for i in range(len(sql_file)):
        if len(sql_file[i]) > 10:
            sql_file[i] += ';'
    table = []
    schema = []
    for s in sql_file:
        m = re.search(r"(create|CREATE)(\s)+(table|TABLE)", s)
        if m:
            table.append(s[m.start():])
            s = s[m.start() + 6:]
            schema.append(only_table(s))
    if schema:
        schema = clear_schema(schema)
    return schema, sql_file, table


def change_to_dict(dic, schema):
    c = copy.deepcopy({k: v for k, v in schema.items() if k in dic})
    change = copy.deepcopy(dict(c))
    for k, v in c.items():
        for it in v.keys():
            if v[it] not in dic[k]:
                del change[k][it]
    return change


def send_change(schema):
    param = []
    dic = {}
    keys = [key for key in schema.keys()]
    for key in keys:
        param.append([schema[key][p] for p in schema[key].keys()])
    for i in range(2, len(sys.argv)):
        m = re.search(r"^(?P<s_name>.+):(?P<param>.+)$", sys.argv[i])
        if m:
            if m.group('s_name') in keys:
                ok = 0
                for p in param:
                    if m.group('param') in p:
                        ok = 1
                        try:
                            if m.group('param') not in dic[m.group('s_name')]:
                                dic[m.group('s_name')].append(m.group('param'))
                        except KeyError:
                            dic[m.group('s_name')] = []
                            dic[m.group('s_name')].append(m.group('param'))
                        break
                if ok == 0:
                    print("Invalid PARAMETER, ( " + m.group('param') + " ) doesn't exist in " + m.group('s_name'))
                    sys.exit(2)
            else:
                print("Invalid PARAMETER ( " + m.group('s_name') + " ) doesn't exist as a table's name")
                sys.exit(2)
        else:
            print("SCHEMA and PARAMETER can't be empty")
            sys.exit(2)
    return change_to_dict(dic, schema)
