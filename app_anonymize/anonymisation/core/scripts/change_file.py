from faker import Faker
from os.path import join
from anonymisation.settings import MEDIA_ROOT
from anonymisation.core.scripts.sql_parse import send_name

import random
import string
import re
import os


def handle_error(pos, length, param, fake, gender):
    print("error")
    param.print_table()
    # log expected
    return ""


def change_char(pos, length, param, fake, gender):
    var = ""
    if param.precision == 0:
        var = "NULL"
    elif "GENDER" in param.name.upper() or "SEX" in param.name.upper():
        var = 'Male' if gender == 0 else "Female"
    elif "NAME" in param.name.upper():
        if "FULL" in param.name.upper():
            var = fake.name_male() if gender == 0 else fake.name_female()
        elif "FIRST" in param.name.upper():
            var = fake.first_name_male() if gender == 0 else fake.first_name_female()
        elif "LAST" in param.name.upper():
            var = fake.last_name()
        elif "USER" in param.name.upper():
            var = fake.first_name_male() if gender == 0 else fake.first_name_female()
            var += str(fake.random_int(min=0, max=999))
        else:
            var = fake.first_name()
    elif "CITY" in param.name.upper():
        var = fake.city()
    elif "COUNTRY" in param.name.upper() or "AREA" in param.name.upper():
        var = fake.country()
    elif "ZIPCODE" in param.name.upper() or "POSTAL" in param.name.upper():
        var = fake.postcode()
    elif "MAIL" in param.name.upper():
        var = fake.word(ext_word_list=None) + "@gmail.com"
    elif "STREET" in param.name.upper() or "ADDRESS" in param.name.upper():
        var = fake.street_address()
    elif "JOB" in param.name.upper():
        var = fake.job()
    elif "PHONE" in param.name.upper():
        var = fake.phone_number()
    elif "PASSWORD" in param.name.upper():
        var = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits)
                      for _ in range(param.precision)
                      )
    elif "ID" in param.name.upper():
        max_pr = '9' * param.precision
        var = str(random.randint(0, int(max_pr)))
    elif param.precision > 5:
        var = fake.text(max_nb_chars=param.precision)
    else:
        var = fake.word()
    if "NOT NULL" in param.params and param.precision > len(var):
        var += ' ' * (param.precision - len(var))
    if len(var) > param.precision:
        var = var[:param.precision - len(var)]
    var = var.replace("'", " ")
    var = var.replace("\n", " ")
    if var != "NULL":
        var = "'%s'" % var
    if pos == 0 and length == 0:
        return "(%s)" % var
    elif pos == length:
        return " %s)" % var
    return " " + var if pos > 0 else "(" + var


def change_int(pos, length, param, fake, gender):
    var = 0
    if param.auto_increment >= 0:
        param.auto_increment += 1
        var = str(param.auto_increment)
    else:
        max_pr = '9' * param.precision
        var = str(random.randint(0, int(max_pr)))
    if "NOT NULL" in param.params and param.precision > len(var):
        var += ' ' * (param.precision - len(var))
    if pos == 0 and length == 0:
        return "(%s)" % var
    elif pos == length:
        return " %s)" % var
    return " " + var if pos > 0 else "(" + var


def change_time(pos, length, param, fake, gender):
    var = ""
    if "YEAR" in param.name:
        var = fake.year()
    elif "MONTH" in param.name:
        var = fake.month()
    elif "DAY" in param.name:
        var = fake.day()
    elif "TIME" in param.name:
        var = fake.time(pattern="%H:%M:%S", end_datetime=None)
    else:
        var = fake.date(pattern="%Y-%m-%d", end_datetime=None)
    var = "'%s'" % var
    if pos == 0 and length == 0:
        return "(%s)" % var
    elif pos == length:
        return " %s)" % var
    return " " + var if pos > 0 else "(" + var


def change_dec(pos, length, param, fake, gender):
    max_pr = '9' * param.precision if param.precision > 0 else 0
    var = str(random.randint(0, int(max_pr)))
    if param.scale > 0:
        max_s = '9' * param.scale if param.scale > 0 else 0
        var += "." + str(random.randint(0, int(max_s)))
    if "NOT NULL" in param.params and param.precision > len(var):
        var += ' ' * (param.precision - len(var))
    if pos == 0 and length == 0:
        return "(%s)" % var
    elif pos == length:
        return " %s)" % var
    return " " + var if pos > 0 else "(" + var


def change_enum(pos, length, param, fake, gender):
    var = ""
    r = random.randint(0, len(param.enum) - 1)
    var = param.enum[r]
    if "NOT NULL" in param.params and param.precision > len(var):
        var += ' ' * (param.precision - len(var))
    if pos == 0 and length == 0:
        return "(%s)" % var
    elif pos == length:
        return " %s)" % var
    return " " + var if pos > 0 else "(" + var


def text_split(text):
    lst = []
    if "," not in text and "\n" not in text:
        lst.append(text)
        return lst
    i = 0
    tmp = 0
    save = 0
    for i in range(len(text)):
        if text[i] == "'" and text[i - 1] == '(' or text[i] == "'" and text[i - 1] == ' '\
                or text[i] == "'" and text[i + 1] == ',' or text[i] == "'" and text[i + 1] == ')':
            tmp += 1
        elif "," == text[i] and tmp % 2 == 0:
            lst.append(text[save:i])
            save = i + 1
        elif text[i] == ";" and tmp % 2 == 0:
            lst.append(text[save:])
    return lst


def change_param(len_i, len_tot, text, type_to_change, fake):
    func = {'char': change_char, 'int': change_int, 'dec': change_dec, 'date': change_time, 'enum': change_enum,
            'error': handle_error}
    n_text = text_split(text)
    len_text = len(n_text) - 1
    gender = random.randint(0, 1)
    for i in range(0, len(n_text)):
        for param in type_to_change:
            if re.search(r"(\(.+\),)|(\(.+\);)", text):
                if i == param.index and "''" != n_text[i]:
                    text = text.replace(n_text[i], func[param.group](
                        i, len_text, param, fake, gender))
                    break
    if len_i == len_tot and text[len(text) - 1] != ';':
        return text + ";"
    return text + "\n"


def text_to_change(s, type_to_change, fake, insert):
    new_file = ""
    sql = s.split('\n')
    for i, s in enumerate(sql):
        m = insert.search(s)
        if not m and len(s) > 0:
            new_file += change_param(i, len(sql) - 1, s, type_to_change, fake)
        elif len(s) > 0:
            if s[len(s) - 1] == ";":
                r = re.search(r"(values |VALUES )", s)
                new_file += s[:r.start() + 7] + change_param(i, len(sql) - 1, s[r.start():],
                                                             type_to_change, fake)
            else:
                new_file += s + "\n"
        else:
            new_file += s + "\n"
    return new_file


def change_file(type_to_change, sql_file, name_file, insert):
    new_file = ""
    fake = Faker('fr_FR')
    for i, s in enumerate(sql_file):
        m = insert.search(s)
        find_s = re.search(r"(values|VALUES)", s)
        if m and find_s:
            change = 0
            for k in type_to_change.keys():
                me = re.search(r"`(.)+`", s[:find_s.start()])
                s_split = s.split("(", 1)
                if k == send_name(me, s_split):
                    change = 1
                    break
            if change == 1:
                new_file += text_to_change(s, type_to_change[k], fake, insert)
            else:
                new_file += s
        else:
            new_file += s
    path = ""
    try:
        os.mkdir(MEDIA_ROOT + "/anonymised_files")
    except OSError:
        pass
    try:
        path = join(MEDIA_ROOT, "anonymised_files/")
        path = join(path, name_file)
        with open(path, 'wb') as f:
            f.write(bytes(new_file, 'utf-8'))
            f.close()
    except OSError:
        print("Error while tryinge to create/write the file")
    return path
