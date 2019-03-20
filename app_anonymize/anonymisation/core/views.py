from anonymisation.core.models import Document
from anonymisation.core.forms import DocumentForm
from anonymisation.core.scripts.anonymize import run
from anonymisation.settings import BASE_DIR, MEDIA_ROOT
from anonymisation.core.scripts.sql_parse import send_schema
from django.shortcuts import render, redirect, get_object_or_404

import os
import re
import time


def q_to_dict(q):
    return {k: v[0] if len(v) == 1 else v for k, v in q.lists()}


def q_to_int(q):
    d = {k: v[0] for k, v in q.lists()}
    try:
        if d['number_line'].isdigit():
            return int(d['number_line'])
        return 0
    except KeyError:
        return 0


def download(request, doc_id):
    total = time.time()
    lst_change = q_to_dict(request.POST)
    document = get_object_or_404(Document, pk=doc_id)
    name_file, path = run(document, lst_change, 0, 0)
    path = os.path.join(MEDIA_ROOT, path)
    return render(request, 'core/download.html', {
        'name': name_file,
        'file_url': path,
        "time": time.time() - total
    })


def generate_file(request, doc_id):
    if request.method == 'POST':
        total = time.time()
        nb_insert = q_to_int(request.POST)
        document = get_object_or_404(Document, pk=doc_id)
        name_file, path = run(document, [], 1, nb_insert)
        path = os.path.join(MEDIA_ROOT, path)
        return render(request, 'core/generate_file.html', {
            'name': name_file,
            'file_url': path,
            "time": time.time() - total
        })


def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', {'documents': documents})


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {'form': form})


def display_file(request, doc_id):
    if request.method == 'POST':
        document = get_object_or_404(Document, pk=doc_id)
        create = re.compile(r"(create|CREATE)(\s)+(table|TABLE)")
        insert = re.compile(r"(insert|INSERT)(\s)+(into|INTO)")
        schema, tmp, tmp1 = send_schema(document, create, insert)
        return render(request, 'core/display_file.html', {'schema': schema, 'doc_id': doc_id})


def destroy_file(request):
    fold = {'/documents/', '/generated_files/', '/anonymised_files/'}
    for f in fold:
        try:
            files = os.listdir(MEDIA_ROOT + f)
            for rf in files:
                os.remove(MEDIA_ROOT + f + rf)
        except OSError:
            pass
    Document.objects.all().delete()
    return redirect('home')
