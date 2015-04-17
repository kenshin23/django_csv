from django.shortcuts import get_object_or_404, render
# TODO: Remove HttpResponse after removing method stubs
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
# XXX: In case the path to the files is needed in some other way, uncomment:
# from django.conf import settings

from .models import Document, Row, Record
import csv


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

    f = open(document.csvfile.path)
    csv_f = ""
    error = ""
    get_lines = 3

    try:
        sample = f.read(1024)
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
    except Exception as e:
        error = "The file doesn't appear to be a valid CSV file."
        # error += " The error was %s", str(repr(e))
    else:
        has_header = sniffer.has_header(sample)
        f.seek(0)
        csv_f = csv.reader(f, dialect)
        content = [row for row in csv_f]
        if len(content) < get_lines:
            line_count = len(content)
        else:
            line_count = get_lines
    finally:
        f.close()

    context = {
        'document': document,
        'has_header': has_header,
        'content': content[:line_count],
        'line_count': line_count,
        'error_message': error
    }
    return render(request, 'files/select.html', context)


def process(request, document_id):
    d = get_object_or_404(Document, pk=document_id)
    try:
        # Get file processing options:
        action = request.POST.get('action')
        has_header_row = request.POST.get('has_header_row', False)
        has_header_row = True if has_header_row else False
        errors = list()

        if action == 'import_only':
            permanent = True
        else:
            permanent = False

        # Get all the column options:
        column_actions = list()
        ignored_columns = 0
        total_columns = int(request.POST.get('csv_columns'))
        column_positions = range(1, total_columns + 1)
        for column_number in column_positions:
            action = dict()
            current_col = "column_choice" + str(column_number)
            current_choice = request.POST[current_col]
            action["set_key"] = current_choice

            if current_choice == "select":
                # get key value from post
                action["value"] = request.POST.get("key" + str(column_number))
            elif current_choice == "header":
                if has_header_row:
                    action["value"] = ""
                else:
                    action["set_key"] = "ignore"
                    action["value"] = False
                    ignored_columns += 1
            elif current_choice == "custom":
                action["value"] = request.POST.get(
                    "custom_key" + str(column_number))
            elif current_choice == "ignore":
                action["value"] = False
            else:
                raise ValueError("An incorrect option was passed.")
            column_actions.append(action)

        if ignored_columns >= total_columns:
            # Houston, we have a problem.
            err_text = "Cannot import the file, all columns are set to ignore."
            errors.append(err_text)
        else:
            # Open and process CSV file:
            row_counter = 0
            records_ok = 0
            records_ignored = 0
            csv_header = list()

            with open(d.csvfile.path) as f:
                csv_f = csv.reader(f)

                # Skip the header row from importing:
                if has_header_row:
                    csv_header = csv_f.next()

                for row in csv_f:
                    row_counter += 1

                    # Create a new Row object and save it:
                    try:
                        db_row = Row(document_id=d.id, permanent=permanent)
                        db_row.save()
                    except Exception as e:
                        raise e

                    # Now create and save new Records with current Row id:
                    for pos in [x-1 for x in column_positions]:
                        if (column_actions[pos]["set_key"] == "select" or
                                column_actions[pos]["set_key"] == "custom"):
                            doc_key = column_actions[pos]["value"]
                        elif column_actions[pos]["set_key"] == "header":
                            doc_key = csv_header[pos]
                        elif column_actions[pos]["set_key"] == "ignore":
                            records_ignored += 1
                            continue
                        else:
                            pass  # for now. Proper error handling is needed.

                        try:
                            db_record = Record(row_id=db_row.id,
                                               doc_key=doc_key,
                                               doc_value=row[pos])
                            db_record.save()
                        except Exception as e:
                            raise e
                        else:
                            records_ok += 1
                # endfor
            # endwith
    except Exception as e:
        raise e
        # Redisplay the document select form.

        return render(request, 'files/select.html', {
            'document': d,
            'error_message': "An exception was raised.",
        })
    else:
        return HttpResponseRedirect(
            reverse('files:scrub', args=(d.id,)))


def scrub(request, document_id):
    # What this method does is:
    # * Get the results of the import, whether temporary or permanent
    # * Based on user selection, create the CSV file or not, and change
    #   all of the records to permanent true or not.
    response = "You're looking at the last stage of file scrubber for doc %s."
    return HttpResponse(response % document_id)
