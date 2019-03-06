from write_file import change_file
from sql_parser import send_schema, send_change

import sys


class TableSpec:
    def __init__(self, index, table, name, group, typ, precision, scale, params):
        self.index = int(index)
        self.table = table
        self.name = name
        self.group = group
        self.type = typ
        self.precision = precision
        self.scale = scale
        self.params = params

    def print_table(self):
        print("table \n| index:", self.index)
        print("| table : ", self.table)
        print("| name: ", self.name)
        print("| group : ", self.group)
        print("| type: ", self.type)
        print("| precision: ", self.precision)
        print("| scale: ", self.scale)
        print("| params: ", self.params)


def var_type(str_s):
    """

        pas encore : ENUM | BINARY | VARBINARY | BLOB | TINYBLOB | MEDIUMBLOB | SET | SERIAL
                     POLYGON | PATH | POINT | MONEY | MACADDR | LSEG | LINE | BYTEA | CIRCLE
                     BOOL |

    """

    var_int = {'int': ['tinyint', 'smallint', 'mediumint', 'bigint', 'int']}
    var_dec = {'dec': ['decimal', 'numeric', 'float', 'real', 'double']}
    var_char = {'char': ['tinytext', 'mediumtext', 'longtext', 'text', 'varchar', 'char']}
    var_time = {'date': ['date', 'datetime', 'time', 'timestamp', 'year']}

    var = [var_int, var_char, var_dec, var_time]
    for search_var in var:
        for v_t in search_var.keys():
            for type_v in search_var[v_t]:
                if type_v in str_s:
                    if type_v == var[len(var) - 1] and type_v not in str_s:
                        return "error", "error"
                    return v_t, type_v
    return "error", "error"


def fill_spec(index, table, name, str_s, spec):
    if len(spec) > 0:
        for n in range(0, len(spec)):
            if spec[n] and spec[n].name == name or str_s[0] == "KEY" or str_s[1] == "KEY"\
                    or str_s[0] == "CONSTRAINT" or str_s[1] == "CONSTRAINT":
                return TableSpec(0, "error", "", "error", "", 0, 0, 0)
    group, v_t = var_type(str_s[1])
    if group == "date":
        return TableSpec(index, table, name, group, v_t, 0, 0,  str_s[2])
    preci = str_s[1][str_s[1].find('('):str_s[1].find(')')]
    if not preci:
        if len(str_s) > 2 and "NOT NULL" not in str_s[2]:
                preci = 0
        else:
            preci = 255
        return TableSpec(index, table,  name, group, v_t, preci, 0, "" if len(str_s) == 2 else str_s[2])
    scale = 0
    if group == "dec":
        preci = str_s[1][str_s[1].find('('):str_s[1].find(',')]
        scale = str_s[1][str_s[1].find(',') + 1:-1]
    return TableSpec(index, table, name, group, v_t, int(preci[1:]), int(scale), str_s[2])


def sort_spec(spec, table):
    for s in spec:
        if s.table != table:
            spec.remove(s)
    return spec


def select_type(schema, name):
    final = {}
    for s_k in schema.keys():
        s_name = name[s_k].split('\n')
        del s_name[0], s_name[-1]
        spec = []
        for i in range(0, len(s_name)):
            for table in schema[s_k]:
                if s_name[i].find(str(schema[s_k][table])) >= 0:
                    test = fill_spec(i, s_k, schema[s_k][table], s_name[i][2:].split(' ', 2), spec)
                    if test.group != "error":
                        spec.append(test)
        final[s_k] = sort_spec(spec, s_k)
    return final


def prepare_change(schema, name, changes):
    i = 0
    new = {}
    for c_k in changes.keys():
        for n in name.keys():
            if n == c_k:
                break
            i += 1
        new_schema = {}
        for l_k in changes[c_k]:
            new_schema[l_k] = str(schema[i][int(l_k)])
        new[n] = new_schema
        i = 0
    return new


def usage():
    print("Usage: py anonymize.py FILE \"SCHEMA:PARAMETER\""
          + "Anonymized every SCHEMA 's PARAMETER in the FILE"
          + "FILE must be a SQL file (.sql)"
          + "MUST have at least ONE key-item \"SCHEMA:PARAMETER\""
          + "\n-c, copy the file and create a new one anonymized")
    sys.exit(2)


def anonymize(schema, name, changes, doc_id):
    schema = prepare_change(schema, name, changes)
    type_to_change = select_type(schema, name)
    name_file, file = change_file(type_to_change, doc_id)
    return name_file[name_file.find('/') + 1:name_file.find('.')] + "_anonymize.sql", file


def main():
    if __name__ == "__main__":
        if len(sys.argv) < 3 and sys.argv[1][:-4] == ".sql":
            return usage()
        schema, name = send_schema(sys.argv[2])
        if schema and name:
            change = send_change(schema)
            if change:
                anonymize()
            else:
                print("No key-items to anonymize")
                sys.exit(2)
        else:
            print("The file is not a SQL file or is an invalid one")
            sys.exit(2)
