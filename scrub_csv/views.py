from django.shortcuts import get_object_or_404, render
# TODO: Remove HttpResponse after removing method stubs
from django.http import HttpResponse
from django.conf import settings

from .models import Document


def index(request):
    latest_document_list = Document.objects.order_by('-upload_date')[:5]
    context = {
        'latest_document_list': latest_document_list,
    }
    return render(request, 'files/index.html', context)


def new(request):
    return HttpResponse("You're looking at the file upload page.")


def detail(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    return render(request, 'files/detail.html', {'document': document})


def records(request, document_id):
    response = "You're looking at the records of document %s."
    return HttpResponse(response % document_id)


def select_fields(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    import csv

    print "Complete path to file: %s" % document.csvfile.path
    f = open(document.csvfile.path)
    csv_f = ""
    error = ""

    try:
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        csv_f = csv.reader(f)
    except Exception as e:
        error = "The file doesn't appear to be a valid CSV file."
        # error += " The error was %s", str(repr(e))

    context = {
        'document': document,
        'lines': csv_f,
        'error_message': error
    }
    return render(request, 'files/select.html', context)


def process(request, document_id):
    response = "This is step 2 for the document %s processing page."
    return HttpResponse(response % document_id)
