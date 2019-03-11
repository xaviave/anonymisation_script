import time


class TableSpec:
    def __init__(self, index, table, name, group, typ, precision, scale):
        self.index = int(index)
        self.table = table
        self.name = name
        self.group = group
        self.type = typ
        self.precision = precision
        self.scale = scale
        self.auto_increment = -1
        self.params = ""

    def init_increment(self):
        if "AUTO_INCREMENT" in self.params or "auto_increment" in self.params:
            self.auto_increment = 0

    def fill_param(self, s):
        if len(s) > 2:
            self.params = s[2]
        if self.params:
            self.init_increment()
        return self

    def print_table(self):
        print("\ntable \n| index : " + str(self.index))
        print("| table : " + str(self.table))
        print("| name: " + str(self.name))
        print("| group : " + str(self.group))
        print("| type: " + str(self.type))
        print("| precision: " + str(self.precision))
        print("| scale: " + str(self.scale))
        print("| params: " + str(self.params))


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
            if spec[n] and spec[n].name == name or str_s[0] == "KEY" or str_s[1] == "KEY" \
                    or str_s[0] == "CONSTRAINT" or str_s[1] == "CONSTRAINT":
                tmp = TableSpec(0, "error", "", "error", "", 0, 0)
                return tmp.fill_param(str_s)
    group, v_t = var_type(str_s[1].lower())
    if group == "date":
        tmp = TableSpec(index, table, name, group, v_t, 0, 0)
        return tmp.fill_param(str_s)
    preci = str_s[1][str_s[1].find('('):str_s[1].find(')')]
    if not preci:
        if len(str_s) > 2:
            if "NOT NULL" not in str_s[2]:
                preci = 0
            tmp = TableSpec(index, table, name, group, v_t, preci, 0)
            return tmp.fill_param(str_s)
        else:
            preci = 16 if group == "int" or group == "dec" else 255
            tmp = TableSpec(index, table, name, group, v_t, preci, 0)
            return tmp.fill_param(str_s)
    scale = 0
    if group == "dec":
        preci = str_s[1][str_s[1].find('('):str_s[1].find(',')]
        scale = str_s[1][str_s[1].find(',') + 1:-1]
    tmp = TableSpec(index, table, name, group, v_t, int(preci[1:]), int(scale))
    return tmp.fill_param(str_s)


def send_change_class(t, change, table):
    li = []
    for c in change.keys():
        for line in t:
            if change[c] in line:
                line = line.strip()
                li.append(fill_spec(c, table, change[c], line.split(' ', 2), li))
                break
    return li


def prepare_change(change, table):
    start = time.time()
    type_to_change = {}
    for c in change.keys():
        for t in table:
            if c in t[0]:
                type_to_change[c] = send_change_class(t, change[c], c)
                break
    print("func: prepare_change = " + str(time.time() - start))
    return type_to_change
