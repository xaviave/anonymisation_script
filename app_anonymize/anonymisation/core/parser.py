import re

from functools import reduce


def send_file(document):
    with document.document.file.open() as fd:
        file = fd.read()
        fd.close()
        return file.decode('utf-8')


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


def send_schema(document):
    sql_file = send_file(document).split(';')
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
    return schema
