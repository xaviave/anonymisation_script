import re
import sys
import copy

from functools import reduce


def send_file(doc):
    with open(doc) as fd:
        sql_file = fd.read()
        fd.close()
    return sql_file


def var_line(line):
    var_int = {'int': ['bool', 'tinyint', 'smallint', 'mediumint', 'bigint', 'int']}
    var_dec = {'dec': ['decimal', 'numeric', 'float', 'real', 'double']}
    var_char = {'char': ['tinytext', 'mediumtext', 'longtext', 'text', 'varchar', 'char']}
    var_time = {'date': ['date', 'datetime', 'time', 'timestamp', 'year']}
    var_enum = {'enum': ['enum']}

    var = [var_int, var_char, var_dec, var_time, var_enum]
    for search_var in var:
        for v_t in search_var.keys():
            for type_v in search_var[v_t]:
                if type_v.upper() in line.upper():
                    if type_v == var[len(var) - 1] and type_v.upper() not in line.upper():
                        return 0
                    return 1
    return 0


def send_table_arg(s):
    i = 0
    par = 0
    save_i = -1
    for i in range(len(s)):
        if "(" == s[i]:
            if par == 0 and save_i == -1:
                save_i = i
            par += 1
        if ")" == s[i]:
            par -= 1
            if save_i > -1 and par == 0:
                break
    if par == 0 and i > 0 and save_i > 0:
        return s[save_i + 1:i]
    else:
        print("Error in TABLE define")
        sys.exit(2)


def send_name(m, s_split):
    not_ex = 0
    if "IF NOT EXISTS" in s_split[0].upper():
        not_ex = 1
    tmp_s = s_split[0].split()
    for i, tmp in enumerate(tmp_s):
        if not_ex == 1 and tmp.upper() == "EXISTS" and i + 1 < len(tmp_s):
            return tmp_s[i + 1] if not m else tmp_s[i + 1][1:-1]
        elif not_ex == 0 and tmp.upper() == "TABLE" and i + 1 < len(tmp_s):
            return tmp_s[i + 1] if not m else tmp_s[i + 1][1:-1]
        elif not_ex == 0 and tmp.upper() == "INTO" and i + 1 < len(tmp_s):
            return tmp_s[i + 1] if not m else tmp_s[i + 1][1:-1]
    return ""


def only_table(s):
    li = []
    s_split = s.split("(", 1)
    m = re.search(r"`(.)+`", s_split[0])
    li.append(send_name(m, s_split))
    s = send_table_arg(s).split(",")
    for i, line in enumerate(s):
        line = line.strip(' ')
        if var_line(line) == 1:
            m = re.search(r"`(.)+`", line)
            k = re.search(r"\bKEY\b", line.upper())
            if m and k and ';' not in line:
                tmp_line = line.split(',', 2)
                if len(tmp_line) > 2:
                    if "KEY" not in tmp_line[0].upper() and "KEY" not in tmp_line[1].upper():
                        li.append(m.group()[1:-1])
            elif m and not k and ';' not in line:
                li.append(m.group()[1:-1])
            elif k and len(line) > 4 and ';' not in line:
                tmp_line = line.split(' ', 2)
                if len(tmp_line) > 1:
                    if "KEY" not in tmp_line[0].upper() and "KEY" not in tmp_line[1].upper():
                        li.append(line.strip().split(' ', 1)[0])
            elif not k and len(line) > 4 and ';' not in line:
                li.append(line.strip().split(' ', 1)[0])
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


def send_schema(create, insert):
    sql_file = send_file(sys.argv[1]).split(';')
    for i in range(len(sql_file)):
        m = create.search(sql_file[i])
        m2 = insert.search(sql_file[i])
        if m or m2:
            sql_file[i] += ';'
    table = []
    schema = []
    for s in sql_file:
        m = create.search(s)
        if m:
            table.append(s[m.start():])
            s = s[m.start() + 6:]
            schema.append(only_table(s))
    if schema:
        schema = clear_schema(schema)
    return schema, sql_file, table


def clean_table(table, change):
    new_t = {}
    for t in table:
        tmp = send_table_arg(t)
        for c in change.keys():
            s_split = t.split("(", 1)
            if c == send_name(re.search(r"`(.)+`", s_split[0]), s_split):
                new_t[c] = tmp
    return new_t


def send_schema_wid(schema):
    change = {}
    for s in schema.keys():
        tmp = {}
        for k, v in schema[s].items():
            if v.upper() != "ID" and "_ID" not in v.upper() and "ID_" not in v.upper():
                tmp[k] = v
        change[s] = tmp
    return change


def change_to_dict(dic, schema):
    c = copy.deepcopy({k: v for k, v in schema.items() if k in dic})
    change = {}
    for k, v in c.items():
        tmp_c = {}
        for it in v.keys():
            for tmp in dic[k]:
                static_f = len(tmp)
                if '=' in tmp:
                    static_f = tmp.find('=')
                if v[it] == tmp[:static_f]:
                    tmp_c[it] = tmp
        if len(tmp_c) > 0:
            change[k] = tmp_c
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
            static_f = len(m.group('param'))
            if '=' in m.group('param'):
                static_f = m.group('param').find('=')
            if m.group('s_name') in keys:
                ok = 0
                for p in param:
                    if m.group('param')[:static_f] in p:
                        ok = 1
                        try:
                            if m.group('param')[:static_f] not in dic[m.group('s_name')]:
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
    if not dic:
        print("SCHEMA and PARAMETER can't be empty")
        sys.exit(2)
    return change_to_dict(dic, schema)
