from django.shortcuts import get_object_or_404
from anonymisation.core.models import Document

from faker import Faker

import sqlparse
import random
import string


def handle_error():
    print("error")
    #log expected
    return ""


def change_char(pos, nu, length, param, fake, gender):
    var = ""
    if param.preci == 0:
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
            var = fake.word()
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
        return change_int(pos, nu, length, param, fake, gender)
    elif param.precision > 5:
        var = fake.text(max_nb_chars=param.precision)
    else:
        var = fake.word()
    if "NOT NULL" in param.params and param.precision > len(var):
        var += ' ' * (param.precision - len(var))
    if len(var) > param.precision:
        var = var[:param.precision - len(var)]
    if var != "NULL":
        var = "'%s'" % var
    if pos == length:
        return " %s)" % var
    return " " + var if pos > 0 else "(" + var


def change_int(pos, nu, length, param, fake, gender):
    var = 0
    if "AUTO_INCREMENT" in param.params:
        var = str(nu)
    else:
        max_pr = '9' * param.precision
        var = str(fake.random_int(min=0, max=int(max_pr)))
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
    var = str(fake.random_int(min=0, max=int(max_pr)))
    if param.scale > 0:
        max_s = '9' * param.scale if param.scale > 0 else 0
        var += "." + str(fake.random_int(min=0, max=int(max_s)))
    if "NOT NULL" in param.params and param.precision > len(var):
        var += ' ' * (param.precision - len(var))
    if pos == length:
        return " %s)" % var
    return " " + var if pos > 0 else "(" + var


def change_param(len_i, len_tot, text, type_to_change, fake):
    n_text = text.split(",")
    len_text = len(n_text) - 1
    if len_i != len_tot:
        len_text -= 1
    func = {'char': change_char, 'int': change_int, 'dec': change_dec, 'date': change_time, 'error': handle_error}
    for i in range(0, len(n_text)):
        gender = random.randint(0, 1)
        for param in type_to_change:
            if i == param.index:
                if "''" != n_text[i]:
                    text = text.replace(n_text[i], func[param.group](i, len_i, len_text, param, fake, gender))
                    break
    if len_tot == len_i:
        text = text + ";"
    return text


def send_change_file(type_to_change, text_to_change, sql, fake):
    text_split = text_to_change.split("\n")
    del text_split[0]
    len_sql = len(text_split) - 1
    for i, text in enumerate(text_split):
        new_t = change_param(i, len_sql, text, type_to_change, fake)
        sql = sql.replace(text, new_t)
    return sql


import time


def change_file(type_to_change, doc_id):
    """

            PART 1

    """
    start = time.time()
    doc = get_object_or_404(Document, pk=doc_id)
    with doc.document.file.open() as fd:
        file = fd.read()
    sql_tuple = sqlparse.parse(file)
    fd.close()
    text_to_change = {}
    sql = ""
    for s in sql_tuple:
        s = str(s)
        sql = sql + s
        if s.find("INSERT INTO") > 0:
            test = s[s.find("INSERT INTO"):].split("`", 2)
            text_to_change[test[1]] = test[2]
    end = time.time()
    print("part 1: change file | ", end - start)
    """
    
            PART 2
    
    """
    start = time.time()
    fake = Faker('fr_FR')
    for k_type in type_to_change.keys():
        for t in text_to_change:
            if t == k_type:
                sql = send_change_file(type_to_change[t], text_to_change[t], sql, fake)
    end = time.time()
    print("part 2 : change_file | ", end - start)
    return doc.document.name, sql
