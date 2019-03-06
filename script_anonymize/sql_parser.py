from os.path import join
from anonymize import anonymize

import re


def only_table(s):
    li = []
    s = s.split(" ")
    for line in s:
        if line.count('`'):
            li.append(line.split("`")[1])
    return li


def send_file(document):
    with document.document.file.open() as fd:
        file = fd.read()
        fd.close()
        return file


def clear_schema(schema):
    dic = {}
    s = []
    for i in range(0, len(schema)):
        del schema[i][0]
        schema[i] = sorted(set(schema[i]))
        d_id = 0
        dic.clear()
        for x in schema[i]:
            dic[d_id] = x
            d_id += 1
        s.append(dict(dic))
    return s


def sql_parse(file):
    file = file.decode("utf-8")
    sql = file.split(";")
    for s in sql:
        m = 0
        v = 0
        for i in range(0, len(s)):
            if m == 0 and s[i] == "\\'":
                m = 1
            else:
                m = 0
                s = s[:int(i)] + ' ' + s[int(i) + 1:]
            if v == 0 and s[i] == ",":
                v = 1
            else:
                v = 0
                s = s[:int(i)] + ' ' + s[int(i) + 1:]
    return sql


g_schema = []
g_name = {}
g_doc_id = 0


def send_schema(document):
    sql = sql_parse(send_file(document))
    schema = []
    name = {}
    for s in sql:
        s = str(s)
        m = re.search(r"(create|CREATE)(\s)+(table|TABLE)", s)
        if m:
            s = s[m.start() + 5:]
            schema.append(only_table(s))
            name[schema[len(schema) - 1][0]] = s
    if schema:
        schema = clear_schema(schema)
    return schema, name


def q_to_dict(q):
    if q:
        return {k: v[0] if len(v) == 1 else v for k, v in q.lists()}
    else:
        return {}


import time


def send_change(schema):
    pass


def download(request):
    start = time.time()
    changes = q_to_dict(request.POST)
    name = dict(g_name)
    schema = list(g_schema)
    name_file, file = anonymize(schema, name, changes)
    end = time.time()
    path = join(MEDIA_ROOT, name_file)
    with open(path, 'w') as f:
        f.write(file)
    f.close()
    print("The file : ", )