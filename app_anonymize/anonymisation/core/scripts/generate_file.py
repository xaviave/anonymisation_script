import random
import threading
import queue
import os

from faker import Faker
from os.path import join
from anonymisation.settings import MEDIA_ROOT
from anonymisation.core.scripts.change_file import change_int, change_dec, change_char, change_time, change_enum, \
    handle_error


def run_thread(tilt, nb_insert, type_to_change, param, my_queue_lst):
    file_2 = generate_file(tilt, nb_insert, type_to_change, param, "")
    my_queue_lst.put(file_2)


def list_param(type_to_change, tilt):
    param = " ("
    for table in type_to_change:
        if tilt == 1:
            param += "`"
        param += table.name
        param += "`, " if tilt == 1 else ", "
    param = param[:-2] + ") VALUES\n"
    return param


def generate_file(tilt, nb_insert, type_to_change, param, new_file):
    func = {'char': change_char, 'int': change_int, 'dec': change_dec, 'date': change_time,
            'enum': change_enum, 'error': handle_error}
    fake = Faker('fr_FR')
    new_file += "\n\nINSERT INTO "
    new_file += "`" if tilt == 1 else ""
    new_file += param
    new_file += "`" if tilt == 1 else ""
    new_file += list_param(type_to_change, tilt)
    len_text = len(type_to_change)
    for i in range(nb_insert):
        for nu, table in enumerate(type_to_change):
            gender = random.randint(0, 1)
            new_file += func[table.group](nu, len_text, table, fake, gender)
            new_file += "," if (nu + 1) < len(type_to_change) else ""
        new_file += "),\n" if i < nb_insert - 1 else ");\n"
    return new_file + "\n"


def generate_db(type_to_change, sql_file, nb_insert, create, name_file):
    new_file = ""
    for l in sql_file:
        new_file += str(l)
    m = create.search(new_file)
    st = new_file[m.start():].split('`', 1)
    tilt = 0
    if len(st) == 2:
        tilt = 1
    if len(type_to_change) > 1:
        my_thread = []
        my_queue_lst = []
        for i, param in enumerate(type_to_change):
            my_queue_lst.append(queue.Queue())
            my_thread.append(
                threading.Thread(run_thread(tilt, nb_insert, type_to_change[param], param, my_queue_lst[i])))
            my_thread[i].start()
    else:
        for param in type_to_change.keys():
            new_file = generate_file(tilt, nb_insert, type_to_change[param], param, new_file)
    path = ""
    try:
        os.mkdir(MEDIA_ROOT + "/generated_files/")
    except OSError:
        pass
    try:
        path = join(MEDIA_ROOT, "generated_files/")
        path = join(path, name_file)
        with open(path, 'wb') as f:
            f.write(bytes(new_file, 'utf-8'))
            if len(type_to_change) > 1:
                for i in range(len(my_thread)):
                    f.write(bytes(my_queue_lst[i].get(), 'utf-8'))
    except OSError:
        print("Error while tryinge to create/write the file")
    return path
