from anonymisation.core.models import Document
from anonymisation.core.forms import DocumentForm
from anonymisation.core.scripts.anonymize import run
from anonymisation.settings import BASE_DIR, MEDIA_ROOT, MEDIA_URL
from anonymisation.core.scripts.sql_parse import send_schema
from django.shortcuts import render, redirect, get_object_or_404

import os
import re
import time


def download(request, doc_id):
    total = time.time()
    document = get_object_or_404(Document, pk=doc_id)
    force = 0
    all_db = 0
    try:
        if request.POST.get('all_db') and request.POST.get('all_db').isdigit():
            all_db = int(request.POST.get('all_db'))
    except KeyError:
        all_db = 0
        try:
            if request.POST.get('force') and request.POST.get('force').isdigit():
                force = int(request.POST.get('force'))
        except KeyError:
            force = 0
    name_file = run(document, request, 0, 0, all_db, force)
    path = os.path.join(MEDIA_URL, "anonymized_files/")
    path = os.path.join(path, name_file)
    return render(request, 'core/download.html', {
        'name': name_file,
        'file_url': path,
        "time": time.time() - total
    })


def generate_file(request, doc_id):
    if request.method == 'POST':
        total = time.time()
        document = get_object_or_404(Document, pk=doc_id)
        nb_insert = 0
        try:
            if request.POST.get('number_line') and request.POST.get('number_line').isdigit():
                nb_insert = int(request.POST.get('number_line'))
        except KeyError:
            return home(request)
        if nb_insert < 1:
            return home(request)
        name_file = run(document, None, 1, nb_insert, 0, 0)
        path = os.path.join(MEDIA_URL, "generated_files/")
        path = os.path.join(path, name_file)
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
    fold = {'/documents/', '/generated_files/', '/anonymized_files/'}
    for f in fold:
        try:
            files = os.listdir(MEDIA_ROOT + f)
            for rf in files:
                os.remove(MEDIA_ROOT + f + rf)
        except OSError:
            pass
    Document.objects.all().delete()
    return redirect('home')
