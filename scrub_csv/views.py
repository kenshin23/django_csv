from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the scrubber index.")


def new(request):
    return HttpResponse("You're looking at the file upload page.")


def detail(request, document_id):
    return HttpResponse("You're looking at file %s." % document_id)


def records(request, document_id):
    response = "You're looking at the records of document %s."
    return HttpResponse(response % document_id)


def select_fields(request, document_id):
    response = "This is step 1 for the document %s processing page."
    return HttpResponse(response % document_id)


def process(request, document_id):
    response = "This is step 2 for the document %s processing page."
    return HttpResponse(response % document_id)
