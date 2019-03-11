from faker import Faker

import random
import string
import os
import sys
import re


def handle_error():
    print("error")
    # log expected
    return ""


def change_char(pos, nu, length, param, fake, gender):
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
        var = fake.postalcode(state_abbr=None)
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
    if var != "NULL":
        var = "'%s'" % var
    if pos == length:
        return " %s)" % var
    return " " + var if pos > 0 else "(" + var


def change_int(pos, nu, length, param, fake, gender):
    var = 0
    if param.auto_increment >= 0:
        param.auto_increment += 1
        var = str(param.auto_increment)
    else:
        max_pr = '9' * param.precision
        var = str(random.randint(0, int(max_pr)))
    if "NOT NULL" in param.params and param.precision > len(var):
        var += ' ' * (param.precision - len(var))
    if pos == length:
        return " %s)" % var
    return " " + var if pos > 0 else "(" + var


def change_time(pos, nu, length, param, fake, gender):
    var = ""
    if "YEAR" in param.name:
        var = fake.year()
    elif "MONTH" in param.name:
        var = fake.month()
    elif "DAY" in param.name:
        var = fake.day()
    elif "TIME" in param.name:
        var = fake.time(pattern="%H:%M:%S", end_datetime=None)
    elif "DATE" in param.name:
        var = fake.date(pattern="%Y-%m-%d", end_datetime=None)
    else:
        var = fake.day_of_month()
    var = "'%s'" % var
    if pos == length:
        return " %s)" % var
    return " " + var if pos > 0 else "(" + var


def change_dec(pos, nu, length, param, fake, gender):
    max_pr = '9' * param.precision if param.precision > 0 else 0
    var = str(random.randint(0, int(max_pr)))
    if param.scale > 0:
        max_s = '9' * param.scale if param.scale > 0 else 0
        var += "." + str(random.randint(0, int(max_s)))
    if "NOT NULL" in param.params and param.precision > len(var):
        var += ' ' * (param.precision - len(var))
    if pos == length:
        return " %s)" % var
    return " " + var if pos > 0 else "(" + var


def change_param(len_i, len_tot, text, type_to_change, fake):  # function a refaire
    n_text = text.split(",")
    len_text = len(n_text) - 1
    if len_i != len_tot:
        len_text -= 1
    func = {'char': change_char, 'int': change_int, 'dec': change_dec, 'date': change_time, 'error': handle_error}
    gender = random.randint(0, 1)
    for i in range(0, len(n_text)):
        for param in type_to_change:
            if re.search(r"(\(.+\),)|(\(.+\);)", text):
                if i == param.index and "''" != n_text[i]:
                    text = text.replace(n_text[i], func[param.group](
                        i, len_i, len_text, param, fake, gender))
                    break
    if len_i == len_tot and text[len(text) - 1] != ';':
        return text + ";"
    return text + "\n"


import time


def text_to_change(s, type_to_change, f, fake):
    sql = s.split('\n')
    for i, s in enumerate(sql):
        m = re.search(r"(insert|INSERT)(\s)+(into|INTO)", s)
        if not m and len(s) > 0:
            f.write(bytes(change_param(i, len(sql) - 1, s, type_to_change, fake), 'utf-8'))
        elif len(s) > 0:
            if s[len(s) - 1] == ";":
                r = re.search(r"(values |VALUES )", s)
                f.write(bytes(
                    s[:r.start() + 7] + change_param(i, len(sql) - 1, s[r.start():],
                                                     type_to_change, fake), 'utf-8')
                )
            else:
                f.write(bytes(s + "\n", 'utf-8'))
        else:
            f.write(bytes(s + "\n", 'utf-8'))


def change_file(type_to_change, sql_file):
    start = time.time()
    fake = Faker('fr_FR')
    path = os.path.realpath(sys.argv[1]) + "_anonymize.sql"
    with open(path, 'wb') as f:
        for s in sql_file:
            m = re.search(r"(insert|INSERT)(\s)+(into|INTO)", s)
            find_s = re.search(r"(value|VALUE)", s)
            if m and f:
                change = 0
                for k in type_to_change.keys():
                    if k in s[:find_s.start()]:
                        change = 1
                        break
                if change == 1:
                    text_to_change(s, type_to_change[k], f, fake)
                else:
                    f.write(bytes(s, 'utf-8'))
            else:
                f.write(bytes(s, 'utf-8'))
        f.close()
    print("func: change_file = " + str(time.time() - start))
    return
