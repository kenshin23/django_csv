# TODO: Remove HttpResponse after removing method stubs
from django.http import HttpResponseRedirect, HttpResponse
# XXX: In case the path to the files is needed in some other way, uncomment:
# from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, render_to_response
from django.core.files import File
from django.core.urlresolvers import reverse


import functions

from .models import Uploader, Document, Row, Record
import csv


def index(request, uploader_id):
    u = get_object_or_404(Uploader, pk=uploader_id)
    latest_document_list = Document.objects.filter(uploader=u).\
        order_by('-upload_date')[:5]
    context = {
        'uploader_id': u.id,
        'latest_document_list': latest_document_list,
    }
    return render(request, 'files/index.html', context)


def new(request, uploader_id):
    from django.template import RequestContext
    from .forms import DocumentForm
    import datetime

    uploader = get_object_or_404(Uploader, pk=uploader_id)

    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(uploader=uploader,
                              csvfile=request.FILES['csvfile'],
                              upload_date=datetime.datetime.now())
            newdoc.save()

            # Redirect to the document list after POST
            redirect_context = {
                'uploader_id': uploader.id,
                'document_id': newdoc.id
            }
            return HttpResponseRedirect(
                reverse('files:detail', kwargs=redirect_context)
            )
    else:
        form = DocumentForm()  # A empty, unbound form

    # Render list page with the documents and the form
    context = {
        'form': form,
        'uploader_id': uploader.id,
    }
    return render_to_response('files/new.html', context,
                              context_instance=RequestContext(request))


def detail(request, uploader_id, document_id):
    uploader = get_object_or_404(Uploader, pk=uploader_id)
    document = get_object_or_404(Document, pk=document_id)

    context = {
        'document': document,
        'uploader_id': uploader.id,
    }
    return render(request, 'files/detail.html', context)


def records(request, uploader_id, document_id):
    response = "You're looking at the records of document %s."
    return HttpResponse(response % document_id)


def select_fields(request, uploader_id, document_id):
    uploader = get_object_or_404(Uploader, pk=uploader_id)
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
        'uploader_id': uploader.id,
        'has_header': has_header,
        'content': content[:line_count],
        'line_count': line_count,
        'error_message': error
    }
    return render(request, 'files/select.html', context)


def process(request, uploader_id, document_id):
    u = get_object_or_404(Uploader, pk=uploader_id)
    d = get_object_or_404(Document, pk=document_id)
    try:
        # Get file processing options:
        perform_action = request.POST.get('action')
        has_header_row = request.POST.get('has_header_row', False)
        has_header_row = True if has_header_row else False
        errors = list()

        if perform_action == 'import_only':
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
                    for pos in [x - 1 for x in column_positions]:
                        if (column_actions[pos]["set_key"] == "select" or
                                column_actions[pos]["set_key"] == "custom"):
                            temp_key = column_actions[pos]["value"]
                        elif column_actions[pos]["set_key"] == "header":
                            temp_key = csv_header[pos]
                        elif column_actions[pos]["set_key"] == "ignore":
                            records_ignored += 1
                            continue
                        else:
                            pass  # for now. Proper error handling is needed.

                        temp_key = functions.clean_key(temp_key)
                        doc_key = functions.validate_key(temp_key)

                        try:
                            # If the record to be saved represents an e-mail
                            # (but is not mistakenly selected as email_md5)
                            # also save it encoded as md5:
                            if doc_key == "email":
                                if (functions.is_email(row[pos]) and not
                                        functions.is_md5(row[pos])):
                                    # Save the additional record:
                                    doc_value = functions.string_to_md5(
                                        row[pos])
                                    db_record = Record(row_id=db_row.id,
                                                       doc_key="email_md5",
                                                       doc_value=doc_value)
                                    db_record.save()
                                    records_ok += 1
                                elif functions.is_md5(row[pos]):
                                    # Proceed with normal save after correcting
                                    # wrong selection:
                                    doc_key = "email_md5"
                                else:
                                    # The value is not md5, but is not a valid
                                    # e-mail address either.
                                    pass

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
            'uploader_id': u.id,
            'document': d,
            'error_message': "An exception was raised.",
        })
    else:
        response_kwargs = {
            'uploader_id': u.id,
            'document_id': d.id,
            'action': perform_action,
        }
        messages.success(request, "Correct records: %d" % records_ok)
        messages.success(request, "Ignored records: %d" % records_ignored)
        return HttpResponseRedirect(
            reverse('files:scrub', kwargs=response_kwargs))


def scrub(request, uploader_id, document_id, action):
    # What this method does is:
    # * Get the results of the import, whether temporary or permanent
    # * Based on user selection, create the CSV file or not, and change
    #   all of the records to permanent true or not.
    uploader = get_object_or_404(Uploader, pk=uploader_id)
    document = get_object_or_404(Document, pk=document_id)
    context = {
        'uploader_id': uploader.id,
        'document': document,
        'action': action
    }

    # Scrub the file against the database:
    if action == "scrub_save" or action == "scrub_only":
        # Get the freshly imported records first (while making sure that
        # they have an 'email'/'email_md5' column -- otherwise, this will
        # turn out empty):
        temp_records = Record.objects.filter(row__document_id=document.id,
                                             row__permanent=False).\
            filter(Q(doc_key="email") | Q(doc_key="email_md5"))

        print "temp_records:"
        print temp_records

        # ---------------------------------------------------------------------

        existing_records = Record.objects.filter(row__permanent=True).\
            filter(Q(doc_key="email") | Q(doc_key="email_md5"))

        print "existing_records:"
        print existing_records

        # ---------------------------------------------------------------------

        intersection = temp_records.filter(
            doc_value__in=list(existing_records.values_list(
                "doc_value", flat=True)))

        print "intersection:"
        print intersection

        found_rows = Row.objects.filter(record=intersection).distinct()
        not_found_rows = Row.objects.filter(record=temp_records).exclude(
            record=intersection).distinct()

        print "found_rows:"
        print found_rows
        print "not_found_rows:"
        print not_found_rows

        import json
        # Convert the found rows into CSV format:
        found_content = convert_to_csv(document,
                                       found_rows,
                                       'found_rows')
        print json.dumps(found_content, sort_keys=True,
                         indent=4, separators=(',', ': '))
        not_found_content = convert_to_csv(document,
                                           not_found_rows,
                                           'not_found_rows')
        print json.dumps(not_found_content, sort_keys=True,
                         indent=4, separators=(',', ': '))

        if (not existing_records and "scrub_" in action):
            messages.error(request, "No records found to scrub against.")
            return render(request, 'files/detail.html', context)

        # Now save or discard records:
        # NOTE: If records already exist, do not duplicate them in the
        # database, i.e.: only save the records that weren't found.
        if action == "scrub_save":
            updated = 0
            updated = not_found_rows.update(permanent=True)
            messages.success(request,
                             "Imported {} row(s) to the database.".format(
                                 len(updated)))
        elif action == "scrub_only":
            # Now cleanup after the import:
            to_delete = Row.objects.filter(permanent=False)
            messages.success(request,
                             "Scrubbed {} row(s) against the database".format(
                                 len(to_delete)))
            to_delete.delete()
        else:
            pass
    elif action == "import_only":
        pass
    else:
        messages.error(request, "The selected action is not available.")

    return render(request, 'files/scrub.html', context)


def convert_to_csv(document, row_queryset, file_type):
    import os
    from datetime import datetime
    from django.conf import settings

    if file_type == "found_rows":
        filename = "foundrecords.csv"
    elif file_type == "not_found_rows":
        filename = "missingrecords.csv"
    else:
        pass  # TODO: error, handle this later

    dtime = datetime.now()
    path = os.path.join(settings.MEDIA_ROOT, 'downloads',
                        str(dtime.year), str(dtime.month).zfill(2),
                        str(dtime.day).zfill(2), filename)
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.makedirs(folder)

    csv_header = list()
    csv_content = list()

    # print "Row queryset:"
    # print row_queryset

    for row in row_queryset:
        aux_row_dict = dict()
        record_list = row.record_set.all()
        for record in record_list:
            csv_header.append(record.doc_key)
            aux_row_dict[record.doc_key] = record.doc_value
        csv_content.append(aux_row_dict)

    # print "csv_header:"
    # print repr(csv_header)

    # print "csv_content:"
    # print repr(csv_content)

    with open(path, 'wb') as f:
        df = File(f)
        w = csv.DictWriter(df, csv_header)
        w.writeheader()
        w.writerows(csv_content)

    if file_type == "found_rows":
        document.found_file.name = path
    elif file_type == "not_found_rows":
        document.not_found_file.name = path
    else:
        pass  # TODO: error, handle this later
    document.save()

    return csv_content


def download(request, uploader_id, document_id, file_type):
    document = get_object_or_404(Document, pk=document_id)

    if file_type == "found_file":
        csv_file = document.found_file
        filename = "foundrecords.csv"
    elif file_type == "not_found_file":
        csv_file = document.not_found_file
        filename = "missingrecords.csv"
    else:
        pass  # error, actually.

    response = HttpResponse(csv_file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=' + filename

    return response
