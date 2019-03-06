import re
import sys
from functools import reduce


def send_file(doc):
    with open(doc) as fd:
        file = fd.read()
        fd.close()
    return file


def only_table(s):
    li = []
    s = s.split("\n")
    for line in s:
        m = re.search(r"`(.)+`", line)
        if m and "KEY" not in line:
            li.append(m.group()[1:-1])
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
    file = send_file(sys.argv[1]).split(';')
    for i in range(len(file)):
        if len(file[i]) > 10:
            file[i] += ';'
    schema = []
    for s in file:
        m = re.search(r"(create|CREATE)(\s)+(table|TABLE)", s)
        if m:
            s = s[m.start() + 6:]
            schema.append(only_table(s))
    if schema:
        schema = clear_schema(schema)
    return schema, file


def change_to_dict(dic, schema):
    change = dict(schema)
    keys = [key for key in dic.keys()]
    for c in schema.keys():
        if c not in keys:
            del change[c]
    print(dic)
    return change


def send_change(schema):  # reflechir comment stocker change
    param = []
    dic = {}
    keys = [key for key in schema.keys()]
    for key in keys:
        param.append([schema[key][p] for p in schema[key].keys()])
    for i in range(len(sys.argv)):
        av = {}
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
                    print("Invalid PARAMETER, (", m.group('param'), ") doesn't exist in", m.group('s_name'))
                    sys.exit(2)
            else:
                print("Invalid PARAMETER (", m.group('param'), ") doesn't exist as a table's name")
                sys.exit(2)
    return change_to_dict(dic, schema)
