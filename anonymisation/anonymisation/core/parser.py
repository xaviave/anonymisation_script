import sqlparse

from os.path import join
from django.shortcuts import render
from anonymisation.settings import MEDIA_ROOT
from anonymisation.core.anonymise import anonymize


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


g_schema = []
g_name = {}
g_doc_id = 0


def send_schema(document, doc_id):
    sql = sqlparse.parse(send_file(document))
    schema = []
    name = {}
    for s in sql:
        s = str(s)
        if "CREATE TABLE" in s:
            s = s[s.find("CREATE"):]
            schema.append(only_table(s))
            name[schema[len(schema) - 1][0]] = s
    if schema:
        schema = clear_schema(schema)
    global g_schema
    global g_name
    global g_doc_id
    g_schema = list(schema)
    g_name = dict(name)
    g_doc_id = int(doc_id)
    return schema, name


def q_to_dict(q):
    return {k: v[0] if len(v) == 1 else v for k, v in q.lists()}


import time


def download(request):
    start = time.time()
    changes = q_to_dict(request.POST)
    name = dict(g_name)
    schema = list(g_schema)
    name_file, file = anonymize(schema, name, changes, g_doc_id)
    end = time.time()
    path = join(MEDIA_ROOT, name_file)
    with open(path, 'w') as f:
        f.write(file)
    f.close()
    return render(request, 'core/download.html', {
        'name': name_file,
        'file_url': path,
        "time": end - start
        })
