import re
import sys


class TableSpec:
    def __init__(self, index, table, name, group, typ, precision, scale, static_var):
        self.index = int(index)
        self.table = table
        self.name = name
        self.group = group
        self.type = typ
        self.precision = precision
        self.scale = scale
        self.auto_increment = -1
        self.params = ""
        self.enum = []
        self.static_var = static_var
        self.unique_ok = 0
        self.unique = {}

    def init_increment(self):
        if "AUTO_INCREMENT" in self.params.upper():
            self.auto_increment = 0

    def init_unique(self):
        if "UNIQUE" in self.params.upper() and not self.static_var:
            self.unique_ok = 1

    def fill_param(self, s):
        if len(s) > 2:
            self.params = s[2]
        if self.params:
            self.init_increment()
            self.init_unique()
        return self

    def fill_enum(self, s):
        line = ""
        for i, tmp in enumerate(s):
            if i != 0:
                line += tmp
        m = re.search(r"(ENUM|enum)\(", line)
        if m:
            line = line[m.start() + 5:line.find(")")]
            lst = line.split(',')
            for i, l in enumerate(lst):
                if "'" in l:
                    self.enum.append(l[1:-1])
            if self.static_var and self.static_var not in self.enum:
                print("Error: static_var: ( " + self.static_var + " ) not in the TABLE's enum")
                if "-f" in sys.argv:
                    self.static_var = ""
                    print("FORCE option is activated, a random variable wil be choose from the enum")
                    return self.fill_param(s)
                else:
                    print("static_var is ignored")
                    self.table = "error"
                    self.group = "error"
                    return self
        else:
            self.table = "error"
            self.group = "error"
            return self
        return self.fill_param(s)

    def print_table(self):
        print("\ntable \n| index : " + str(self.index))
        print("| table : " + str(self.table))
        print("| name: " + str(self.name))
        print("| group : " + str(self.group))
        print("| type: " + str(self.type))
        print("| auto_increment: " + str(self.auto_increment))
        print("| precision: " + str(self.precision))
        print("| scale: " + str(self.scale))
        print("| params: " + str(self.params))
        print("| enum: " + str(self.enum))
        print("| static_var: " + str(self.static_var))


def var_type(str_s):
    """

        pas encore : BINARY | VARBINARY | BLOB | TINYBLOB | MEDIUMBLOB | SET | SERIAL
                     POLYGON | PATH | POINT | MONEY | MACADDR | LSEG | LINE | BYTEA | CIRCLE |


    """

    var_int = {'int': ['bool', 'tinyint', 'smallint', 'mediumint', 'bigint', 'int']}
    var_dec = {'dec': ['decimal', 'numeric', 'float', 'real', 'double']}
    var_char = {'char': ['tinytext', 'mediumtext', 'longtext', 'text', 'varchar', 'char']}
    var_time = {'date': ['date', 'datetime', 'time', 'timestamp', 'year']}
    var_enum = {'enum': ['enum']}

    var = [var_int, var_char, var_dec, var_time, var_enum]
    for search_var in var:
        for v_t in search_var.keys():
            for type_v in search_var[v_t]:
                if type_v in str_s:
                    if type_v == var[len(var) - 1] and type_v not in str_s:
                        return "error", "error"
                    return v_t, type_v
    return "error", "error"


def fill_spec(index, table, name, static_var, str_s, spec):
    if len(spec) > 0:
        for n in range(0, len(spec)):
            if spec[n] and len(str_s) > 1:
                if spec[n].name == name or str_s[0] == "KEY" or str_s[1] == "KEY" \
                        or str_s[0] == "CONSTRAINT" or str_s[1] == "CONSTRAINT":
                    tmp = TableSpec(0, "error", "", "error", "", 0, 0, "")
                    return tmp.fill_param(str_s)
    group, v_t = var_type(str_s[1].lower())
    if group == "error":
        tmp = TableSpec(0, "error", "", "error", "", 0, 0, "")
        return tmp.fill_param(str_s)
    if group == "enum":
        tmp = TableSpec(index, table, name, group, v_t, 0, 0, static_var[1:])
        return tmp.fill_enum(str_s)
    if group == "date":
        tmp = TableSpec(index, table, name, group, v_t, 0, 0, static_var[1:])
        return tmp.fill_param(str_s)
    preci = str_s[1][str_s[1].find('('):str_s[1].find(')')]
    if not preci:
        if len(str_s) > 2:
            preci = 1
            if "NOT NULL" not in str_s[2]:
                preci = 1
            tmp = TableSpec(index, table, name, group, v_t, preci, 0, static_var[1:])
            return tmp.fill_param(str_s)
        else:
            preci = 9 if group == "int" or group == "dec" else 255
            tmp = TableSpec(index, table, name, group, v_t, preci, 0, static_var[1:])
            return tmp.fill_param(str_s)
    scale = 0
    if group == "dec":
        preci = str_s[1][str_s[1].find('('):str_s[1].find(',')]
        scale = str_s[1][str_s[1].find(',') + 1:-1]
    if not static_var[1:].isdigit() and (group == 'dec' or group == 'int') and "-f" not in sys.argv:
        static_var = "="
    tmp = TableSpec(index, table, name, group, v_t, int(preci[1:]), int(scale), static_var[1:])
    return tmp.fill_param(str_s)


def send_change_class(t, change, table):
    li = []
    for c in change.keys():
        for line in t:
            static_f = len(change[c])
            if '=' in change[c]:
                static_f = change[c].find('=')
            if change[c][:static_f] in line:
                line = line.strip()
                pattern = re.compile(r'\s+')
                line = re.sub(pattern, ' ', line)
                li.append(fill_spec(c, table, change[c][:static_f], change[c][static_f:], line.split(' ', 2), li))
                break
    return li


def clean_type(type_to_change):
    new_change = {}
    for table in type_to_change.keys():
        for t in type_to_change[table]:
            if t.table != "error":
                try:
                    new_change[table].append(t)
                except KeyError:
                    new_change[table] = []
                    new_change[table].append(t)
    return new_change


def text_split_1(text):
    lst = []
    if "," not in text and "\n" not in text:
        lst.append(text)
        return lst
    i = 0
    tmp = 0
    save = 0
    tmp_2 = 0
    for i in range(len(text)):
        if text[i] == "'" or text[i] == "(" or text[i] == ")":
            if text[i] == "'":
                tmp += 1
            elif text[i] == "(":
                tmp_2 += 1
            elif text[i] == ")":
                tmp_2 -= 1
        elif "," == text[i] and tmp % 2 == 0 and tmp_2 == 0:
            lst.append(text[save:i])
            save = i + 1
        elif text[i] == ";" and tmp % 2 == 0:
            lst.append(text[save:i])
    if save > 0:
        lst.append(text[save + 1:])
    return lst


def prepare_change(change, table):
    type_to_change = {}
    for c in change.keys():
        for t in table.keys():
            if c == t:
                type_to_change[c] = send_change_class(text_split_1(table[t]), change[c], c)
                break
    return clean_type(type_to_change)
