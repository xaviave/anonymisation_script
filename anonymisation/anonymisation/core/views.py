from django.shortcuts import render, redirect, get_object_or_404

from anonymisation.core.models import Document
from anonymisation.core.forms import DocumentForm
from anonymisation.core.parser import send_schema
from anonymisation.settings import BASE_DIR

import os


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
        schema, name = send_schema(document, doc_id)
        return render(request, 'core/display_file.html', {'schema': schema, 'name': name})
    else:
        return render(request, 'core/display_file.html')


def destroy_file(request):
    documents = Document.objects.all()
    for doc in documents:
        if os.path.exists(BASE_DIR + doc.document.url):
            os.remove(BASE_DIR + doc.document.url)
        else:
            print("File : ", BASE_DIR + doc.document.url, " doesn't exist")
    Document.objects.all().delete()
    return redirect('home')
